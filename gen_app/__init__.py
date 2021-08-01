from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join


app = Flask(__name__)
app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'

from gen_app import routes