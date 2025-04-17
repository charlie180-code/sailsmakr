from datetime import datetime
from ... import db

class AccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    archive_id = db.Column(db.Integer, db.ForeignKey('archive.id'))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='access_requests')
    archive = db.relationship('Archive', backref='requests')
