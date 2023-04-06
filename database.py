from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()
db = SQLAlchemy()


class SoundClip(db.Model):
    """
    This table represents sound clips.
    """
    __tablename__ = 'sound_clip'

    id = db.Column(db.Integer(), primary_key=True, unique=True)
    hash = db.Column(db.String())
    file_size_mb = db.Column(db.Float())
    file_name = db.Column(db.String())
    chunk = db.Column(db.Boolean())
    chunk_index = db.Column(db.Integer())
    transcriptions = db.Column(db.String())

    def __repr__(self):
        return f"<SoundClip {self.id}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
