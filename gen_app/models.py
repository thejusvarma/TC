from datetime import datetime
from gen_app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=False,nullable=False)
    issued = db.relationship('Issued',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

# creating posts table
class Issued(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    roll_num = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"Post('{self.date_posted}')"
