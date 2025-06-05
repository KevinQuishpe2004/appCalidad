from models.database import db
from datetime import datetime

class Series(db.Model):
    __tablename__ = 'series'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    therapy_type_id = db.Column(db.Integer, db.ForeignKey('therapy_type.id'), nullable=False)
    total_sessions = db.Column(db.Integer, default=1)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships
    postures = db.relationship('SeriesPosture', backref='series', lazy=True, order_by="SeriesPosture.order")
    sessions = db.relationship('Session', backref='series', lazy=True)
    
    creator = db.relationship(
        'User', 
        foreign_keys=[creator_id],
        back_populates='created_series'
    )

    patient = db.relationship(
        'User', 
        foreign_keys=[patient_id],
        back_populates='assigned_series'
    )
    
    def __repr__(self):
        return f'<Series {self.name}>'
    
    def completed_sessions_count(self):
        return len(self.sessions)
    
    def remaining_sessions(self):
        return max(0, self.total_sessions - self.completed_sessions_count())
    
    def is_complete(self):
        return self.completed_sessions_count() >= self.total_sessions