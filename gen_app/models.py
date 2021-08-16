from datetime import datetime
from gen_app import db,login_manager
from flask_login import UserMixin
import pytz

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=False,nullable=False)
    issued = db.relationship('Issued',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

# creating Issued table
class Issued(db.Model):
    IST = pytz.timezone('Asia/Kolkata')
    id = db.Column(db.Integer,primary_key=True)
    roll_num = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.now(IST))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"Issued('{self.user_id}','{self.roll_num}','{self.date_posted}')" 

