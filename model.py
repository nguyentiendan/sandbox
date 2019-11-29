from datetime import datetime
from config import db, ma

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    fullname = db.Column(db.String(50), index=True)
    ctime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    mtime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session