from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db =  SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='primary'
login_manager.login_message='Please login to access!'

from gen_app import routes