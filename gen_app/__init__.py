from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db =  SQLAlchemy(app)
from gen_app import routes