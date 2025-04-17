from datetime import datetime
from ... import db

class ArchiveAccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    archive_id = db.Column(db.Integer, db.ForeignKey('archive.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(50))  # ex: "viewed", "downloaded"

    archive = db.relationship('Archive', backref='access_logs')
    user = db.relationship('User', backref='archive_accesses')
