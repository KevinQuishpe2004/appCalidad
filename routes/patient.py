from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from models.database import db
from models.user import User
from models.series import Series
from models.series_posture import SeriesPosture
from models.posture import Posture
from models.session import Session
from routes.auth import patient_required
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@patient_required
def dashboard():
    patient = User.query.get(session['user_id'])
    return render_template('patient/dashboard.html', patient=patient)

@patient_bp.route('/series')
@patient_required
def view_series():
    patient = User.query.get(session['user_id'])
    series = patient.assigned_series
    
    if not series:
        flash('You don\'t have any assigned series yet.', 'info')
        return render_template('patient/no_series.html')
    
    return render_template('patient/view_series.html', series=series)

@patient_bp.route('/series/execute', methods=['GET', 'POST'])
@patient_required
def execute_series():
    patient = User.query.get(session['user_id'])
    series = patient.assigned_series
    
    if not series:
        flash('You don\'t have any assigned series yet.', 'info')
        return redirect(url_for('patient.dashboard'))
    
    
    if request.method == 'POST':
        # Process session completion
        pain_level_end = request.form.get('pain_level_end')
        comment = request.form.get('comment')
        
        # Get the session from the database
        session_id = request.form.get('session_id')
        yoga_session = Session.query.get(session_id)
        
        print(f"pain_level_end: {pain_level_end}")
        print(f"comment: {comment}")
        print(f"Session ID from form: {session_id}")
        print(f"Yoga session: {yoga_session}")
          
        if not yoga_session:
            flash('Session not found.', 'error')
            return redirect(url_for('patient.dashboard'))
        
        # Update session data
        yoga_session.end_time = datetime.utcnow()
        yoga_session.pain_level_end = pain_level_end
        yoga_session.comment = comment
        
        # Calculate effective duration in seconds
        if yoga_session.start_time:
            duration = (yoga_session.end_time - yoga_session.start_time).total_seconds()
            yoga_session.effective_duration = int(duration)
        
        db.session.commit()
        flash('Session completed successfully!', 'success')
        return redirect(url_for('patient.dashboard'))
    
    if series.is_complete():
        print(f"Series {series.id} is complete.")
        print(f"Number of sesiones: {series.completed_sessions_count()}")
        print(f"Total sessions required: {series.total_sessions}")
        flash('You have completed all sessions for this series.', 'info')
        return redirect(url_for('patient.dashboard'))
    
    # Starting a new session
    if request.method == 'GET':
        pain_level_start = request.args.get('pain_level')

        if pain_level_start:
            # Create a new session
            yoga_session = Session(
                series_id=series.id,
                patient_id=patient.id,
                pain_level_start=pain_level_start,
                start_time=datetime.utcnow()
            )

            db.session.add(yoga_session)
            db.session.commit()

            # Get all postures in this series
            postures = db.session.query(Posture, SeriesPosture)\
                .join(SeriesPosture, Posture.id == SeriesPosture.posture_id)\
                .filter(SeriesPosture.series_id == series.id)\
                .order_by(SeriesPosture.order)\
                .all()

            return render_template('patient/execute_series.html', 
                                  series=series, 
                                  postures=postures, 
                                  session_id=yoga_session.id)

        # Show pain level selection form
        return render_template('patient/start_session.html', series=series)

@patient_bp.route('/sessions')
@patient_required
def sessions():
    patient = User.query.get(session['user_id'])
    sessions = Session.query.filter_by(patient_id=patient.id).order_by(Session.date.desc()).all()
    return render_template('patient/sessions.html', sessions=sessions)

@patient_bp.route('/session/pause', methods=['POST'])
@patient_required
def pause_session():
    
    session_id = request.json.get('session_id')
    yoga_session = Session.query.get_or_404(session_id)
    
    # Ensure the session belongs to the current patient
    if yoga_session.patient_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Increment pause count
    yoga_session.pause_count += 1
    db.session.commit()
    
    return jsonify({'success': True, 'pause_count': yoga_session.pause_count})