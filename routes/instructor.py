from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.database import db
from models.user import User, InstructorPatient
from models.posture import Posture
from models.therapy_type import TherapyType
from models.series import Series
from models.series_posture import SeriesPosture
from models.session import Session
from routes.auth import instructor_required
from werkzeug.security import generate_password_hash
import json
from datetime import datetime

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor')

@instructor_bp.route('/dashboard')
@instructor_required
def dashboard():
    instructor = User.query.get(session['user_id'])
    patients = instructor.patients.all()
    return render_template('instructor/dashboard.html', instructor=instructor, patients=patients)

@instructor_bp.route('/patients')
@instructor_required
def patients():
    instructor = User.query.get(session['user_id'])
    patients = instructor.patients.all()
    return render_template('instructor/patients.html', patients=patients)

@instructor_bp.route('/patient/add', methods=['GET', 'POST'])
@instructor_required
def add_patient():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')
        
        # Check if username or email already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'error')
            return redirect(url_for('instructor.add_patient'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
            return redirect(url_for('instructor.add_patient'))
        
        # Create new patient
        new_patient = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            name=name,
            role='patient'
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        # Associate patient with instructor
        instructor = User.query.get(session['user_id'])
        instructor.patients.append(new_patient)
        db.session.commit()
        
        flash(f'Patient {name} has been added successfully.', 'success')
        return redirect(url_for('instructor.patients'))
    
    return render_template('instructor/add_patient.html')

@instructor_bp.route('/patient/<int:patient_id>/edit', methods=['GET', 'POST'])
@instructor_required
def edit_patient(patient_id):
    patient = User.query.get_or_404(patient_id)
    instructor = User.query.get(session['user_id'])
    
    # Check if this patient belongs to the instructor
    if patient not in instructor.patients:
        flash('You do not have permission to edit this patient.', 'error')
        return redirect(url_for('instructor.patients'))
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.email = request.form.get('email')
        
        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            patient.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash(f'Patient {patient.name} has been updated successfully.', 'success')
        return redirect(url_for('instructor.patients'))
    
    return render_template('instructor/edit_patient.html', patient=patient)

@instructor_bp.route('/series')
@instructor_required
def series_list():
    instructor = User.query.get(session['user_id'])
    series = Series.query.filter_by(creator_id=instructor.id).all()
    return render_template('instructor/series_list.html', series=series)

@instructor_bp.route('/series/create', methods=['GET', 'POST'])
@instructor_required
def create_series():
    if request.method == 'POST':
        name = request.form.get('name')
        therapy_type_id = request.form.get('therapy_type')
        total_sessions = int(request.form.get('total_sessions'))
        
        # Create new series
        new_series = Series(
            name=name,
            therapy_type_id=therapy_type_id,
            total_sessions=total_sessions,
            creator_id=session['user_id']
        )
        
        db.session.add(new_series)
        db.session.commit()
        
        # Get postures and their durations
        postures_data = json.loads(request.form.get('postures_data'))
        
        for idx, posture_data in enumerate(postures_data):
            posture_id = posture_data['id']
            duration = posture_data['duration']
            
            series_posture = SeriesPosture(
                series_id=new_series.id,
                posture_id=posture_id,
                order=idx + 1,
                duration_minutes=duration
            )
            
            db.session.add(series_posture)
        
        db.session.commit()
        flash(f'Series "{name}" has been created successfully.', 'success')
        return redirect(url_for('instructor.series_list'))
    
    therapy_types = TherapyType.query.all()
    return render_template('instructor/create_series.html', therapy_types=therapy_types)

@instructor_bp.route('/therapy/<int:therapy_id>/postures')
@instructor_required
def get_therapy_postures(therapy_id):
    therapy = TherapyType.query.get_or_404(therapy_id)
    postures = therapy.postures
    postures_data = [{
        'id': posture.id,
        'name': posture.name,
        'sanskrit_name': posture.sanskrit_name,
        'image_url': posture.image_url,
        'description': posture.description
    } for posture in postures]
    
    return {'postures': postures_data}

@instructor_bp.route('/patient/<int:patient_id>/assign_series', methods=['GET', 'POST'])
@instructor_required
def assign_series(patient_id):
    patient = User.query.get_or_404(patient_id)
    instructor = User.query.get(session['user_id'])
    
    # Check if this patient belongs to the instructor
    if patient not in instructor.patients:
        flash('You do not have permission to assign series to this patient.', 'error')
        return redirect(url_for('instructor.patients'))
    
    if request.method == 'POST':
        series_id = request.form.get('series_id')
        series = Series.query.get_or_404(series_id)
        
        # Check if this series belongs to the instructor
        if series.creator_id != instructor.id:
            flash('You do not have permission to assign this series.', 'error')
            return redirect(url_for('instructor.assign_series', patient_id=patient_id))
        
        # If patient already has an assigned series, unassign it
        if patient.assigned_series:
            patient.assigned_series.patient_id = None
        
        # Assign the new series
        series.patient_id = patient.id
        db.session.commit()
        
        flash(f'Series "{series.name}" has been assigned to {patient.name}.', 'success')
        return redirect(url_for('instructor.patient_series', patient_id=patient_id))
    
    # Get all series created by this instructor
    series = Series.query.filter_by(creator_id=instructor.id).all()
    return render_template('instructor/assign_series.html', patient=patient, series=series)

@instructor_bp.route('/patient/<int:patient_id>/series')
@instructor_required
def patient_series(patient_id):
    patient = User.query.get_or_404(patient_id)
    instructor = User.query.get(session['user_id'])
    
    # Check if this patient belongs to the instructor
    if patient not in instructor.patients:
        flash('You do not have permission to view this patient\'s series.', 'error')
        return redirect(url_for('instructor.patients'))
    
    return render_template('instructor/patient_series.html', patient=patient)

@instructor_bp.route('/patient/<int:patient_id>/sessions')
@instructor_required
def patient_sessions(patient_id):
    patient = User.query.get_or_404(patient_id)
    instructor = User.query.get(session['user_id'])
    
    # Check if this patient belongs to the instructor
    if patient not in instructor.patients:
        flash('You do not have permission to view this patient\'s sessions.', 'error')
        return redirect(url_for('instructor.patients'))
    
    sessions = Session.query.filter_by(patient_id=patient_id).order_by(Session.date.desc()).all()
    return render_template('instructor/patient_sessions.html', patient=patient, sessions=sessions)