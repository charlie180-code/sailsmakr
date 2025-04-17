from datetime import datetime
from ... import db

class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))  # ex: "Contrat client", "Relevé", etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_level = db.Column(db.String(50))  # ex: "public", "interne", "confidentiel"

    uploaded_by = db.relationship('User', backref='archives')
