from models.database import db

# Association table for postures and therapy types
posture_therapy = db.Table('posture_therapy',
    db.Column('posture_id', db.Integer, db.ForeignKey('posture.id'), primary_key=True),
    db.Column('therapy_type_id', db.Integer, db.ForeignKey('therapy_type.id'), primary_key=True)
)

class TherapyType(db.Model):
    __tablename__ = 'therapy_type'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    postures = db.relationship('Posture', secondary=posture_therapy, 
                              lazy='subquery', backref=db.backref('therapy_types', lazy=True))
    series = db.relationship('Series', backref='therapy_type', lazy=True)
    
    def __repr__(self):
        return f'<TherapyType {self.name}>'