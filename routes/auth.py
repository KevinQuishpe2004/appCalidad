from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from models.user import User
from functools import wraps
import re

# Blueprint con prefijo '/auth' para todas las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_password_strength(password):
    """
    Valida que la contraseña cumple con los requisitos de seguridad
    Retorna: (es_valida: bool, errores: list)
    """
    errors = []
    
    # Verificar longitud mínima
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    
    # Verificar letra mayúscula
    if not re.search(r"[A-Z]", password):
        errors.append("La contraseña debe contener al menos una letra mayúscula")
    
    # Verificar letra minúscula
    if not re.search(r"[a-z]", password):
        errors.append("La contraseña debe contener al menos una letra minúscula")
    
    # Verificar número
    if not re.search(r"\d", password):
        errors.append("La contraseña debe contener al menos un número")
    
    # Verificar carácter especial
    if not re.search(r"[@$!%*?&]", password):
        errors.append("La contraseña debe contener al menos un carácter especial (@$!%*?&)")
    
    # Verificar que no sea demasiado común
    common_passwords = [
        'password', '12345678', 'qwerty', 'abc123', 'password123',
        '123456789', 'welcome', 'admin123', 'letmein', 'monkey'
    ]
    
    if password.lower() in common_passwords:
        errors.append("Esta contraseña es demasiado común. Elige una más segura")
    
    return len(errors) == 0, errors

def validate_username(username):
    """
    Valida formato del username
    Retorna: (es_valido: bool, error: str)
    """
    if len(username) < 3 or len(username) > 20:
        return False, "El nombre de usuario debe tener entre 3 y 20 caracteres"
    
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, ""

def validate_email_format(email):
    """
    Valida formato del email
    Retorna: (es_valido: bool, error: str)
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Por favor ingresa un email válido"
    
    if len(email) > 256:
        return False, "El email es demasiado largo"
    
    return True, ""

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
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
            return redirect(url_for('main.index'))
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
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Lista para acumular errores
        validation_errors = []
        
        # Validar nombre
        if not name or len(name) < 2 or len(name) > 120:
            validation_errors.append("El nombre debe tener entre 2 y 120 caracteres")
        
        # Validar email
        email_valid, email_error = validate_email_format(email)
        if not email_valid:
            validation_errors.append(email_error)
        
        # Validar username
        username_valid, username_error = validate_username(username)
        if not username_valid:
            validation_errors.append(username_error)
        
        # Validar contraseña
        password_valid, password_errors = validate_password_strength(password)
        if not password_valid:
            validation_errors.extend(password_errors)
        
        # Validar confirmación de contraseña
        if password != confirm_password:
            validation_errors.append("Las contraseñas no coinciden")
        
        # Verificar si el username ya existe
        if User.query.filter_by(username=username).first():
            validation_errors.append("Este nombre de usuario ya está en uso")
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=email).first():
            validation_errors.append("Este correo electrónico ya está registrado")
        
        # Si hay errores, mostrarlos y regresar al formulario
        if validation_errors:
            for error in validation_errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        try:
            # Crear nuevo usuario
            new_user = User(
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                email=email,
                name=name,
                role='instructor'  # Solo instructores pueden registrarse
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('¡Registro exitoso! Ya puedes iniciar sesión con tu cuenta.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validaciones básicas
        if not username or not password:
            flash('Por favor completa todos los campos.', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Nombre de usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('auth.login'))
        
        # Guardar información del usuario en la sesión
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        flash(f'¡Bienvenido de nuevo, {user.name}!', 'success')
        
        # Redireccionar según el rol
        if user.role == 'instructor':
            return redirect(url_for('instructor.dashboard'))
        else:
            return redirect(url_for('patient.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.logout_page'))

@auth_bp.route('/logout-confirmation')
def logout_page():
    return render_template('auth/logout.html')