from models.database import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'session'
    
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    pain_level_start = db.Column(db.String(50), nullable=False)  # none, mild, moderate, intense, maximum
    pain_level_end = db.Column(db.String(50), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    pause_count = db.Column(db.Integer, default=0)
    effective_duration = db.Column(db.Integer, nullable=True)  # in seconds
    
    def __repr__(self):
        return f'<Session {self.id}>'