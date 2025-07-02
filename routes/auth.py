from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from models.user import User
from functools import wraps

# Blueprint con prefijo '/auth' para todas las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))  # Usa el nombre del blueprint
        return f(*args, **kwargs)
    return decorated_function

def instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if user.role != 'instructor':
            flash('Access denied. Instructor privileges required.', 'error')
            return redirect(url_for('main.index'))  # Cambiado a 'main.index'
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if user.role != 'patient':
            flash('Access denied. Patient privileges required.', 'error')
            return redirect(url_for('main.index'))  # Cambiado a 'main.index'
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')
        
        # Check if username or email already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            name=name,
            role='instructor'  # Only instructors can register
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))
        
        # Save user info in session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Redirect based on role
        if user.role == 'instructor':
            return redirect(url_for('instructor.dashboard'))  # Nombre completo del blueprint
        else:
            return redirect(url_for('patient.dashboard'))  # Nombre completo del blueprint
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('auth.logout_page'))  # Redirige a la página de confirmación
@auth_bp.route('/logout-confirmation')
def logout_page():
    return render_template('auth/logout.html')