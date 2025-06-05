from models.database import db

class SeriesPosture(db.Model):
    __tablename__ = 'series_posture'
    
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    posture_id = db.Column(db.Integer, db.ForeignKey('posture.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<SeriesPosture {self.id}>'