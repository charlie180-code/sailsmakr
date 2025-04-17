from ... import db

class ArchiveCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    archives = db.relationship('Archive', backref='category_obj')
