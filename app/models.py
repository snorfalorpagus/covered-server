from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Upload(db.Model):
    id = db.Column(db.String, primary_key=True)
    hit = db.Column(db.Integer)
    missing = db.Column(db.Integer)
    excluded = db.Column(db.Integer)
    total = db.Column(db.Integer)
    coverage_percent = db.Column(db.Float)
    git_branch = db.Column(db.String)
    git_commit = db.Column(db.String)


class SourceFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    source = db.Column(db.String)
    upload_id = db.Column(db.String, db.ForeignKey("upload.id"))
    upload = relationship("Upload", backref="source_files")
    coverage = db.Column(db.String)
    hit = db.Column(db.Integer)
    missing = db.Column(db.Integer)
    excluded = db.Column(db.Integer)
    total = db.Column(db.Integer)
    coverage_percent = db.Column(db.Float)
