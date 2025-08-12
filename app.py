from flask import Flask, render_template, redirect, url_for, flash, request, session
import os
from models.database import init_db, populate_initial_data
from routes.auth import auth_bp
from routes.instructor import instructor_bp
from routes.patient import patient_bp
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yoga_therapy_user:t8evTXerEeA6kT6GmrBK4CQ8Cut0LXdi@dpg-d2d83andiees73fvc5ig-a.oregon-postgres.render.com/yoga_therapy_2bmk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos SIEMPRE
init_db(app)

# Definición de filtros personalizados
def nl2br(value):
    """Convierte saltos de línea en <br> tags de manera segura"""
    if not value:
        return ''
    result = re.sub(r'\r\n|\r|\n', '<br>', str(value))
    return Markup(result)  # Markup marca el string como seguro para HTML

# Registrar filtros en Jinja2
app.jinja_env.filters['nl2br'] = nl2br

# Puedes agregar más filtros si los necesitas
def format_currency(value):
    """Formatea números como moneda"""
    return f"${value:,.2f}"

app.jinja_env.filters['currency'] = format_currency

# Registrar blueprints con prefijos consistentes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(instructor_bp, url_prefix='/instructor')
app.register_blueprint(patient_bp, url_prefix='/patient')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    
    #from models.database import db  # importa la instancia de SQLAlchemy
    # Crear las tablas en la base de datos
    with app.app_context():
        # db.create_all()   
        # Populate initial data if database is empty
        populate_initial_data()
    
    # Run the application
    app.run(debug=True, port=5050)
    