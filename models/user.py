from models.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'instructor' or 'patient'
    
    # Relationships
    # For instructors: patients they manage
    patients = db.relationship('User', 
                              secondary='instructor_patient',
                              primaryjoin="and_(User.id==InstructorPatient.instructor_id, User.role=='instructor')",
                              secondaryjoin="and_(User.id==InstructorPatient.patient_id, User.role=='patient')",
                              backref=db.backref('instructors', lazy='dynamic'),
                              lazy='dynamic')
    
    # Patient's assigned series
    created_series = db.relationship(
        'Series',
        foreign_keys='Series.creator_id',
        back_populates='creator',
        lazy=True
    )
    
    assigned_series = db.relationship(
        'Series',
        foreign_keys='Series.patient_id',
        back_populates='patient',
        lazy=True,
        uselist=False
    )
    
    # Sessions completed by patients
    sessions = db.relationship('Session', backref='patient', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Association table for instructor-patient relationship
class InstructorPatient(db.Model):
    __tablename__ = 'instructor_patient'
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)