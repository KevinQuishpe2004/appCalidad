from models.database import db

class Posture(db.Model):
    __tablename__ = 'posture'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sanskrit_name = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    modifications = db.Column(db.Text, nullable=True)
    
    # Relationships
    series_postures = db.relationship('SeriesPosture', backref='posture', lazy=True)
    
    def __repr__(self):
        return f'<Posture {self.name}>'