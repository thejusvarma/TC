# this file is executed first and its set using command -> $env:FLASK_APP = "run.py"
# change app to development server -> $env:FLASK_ENV = "development" 
# activate debugger -> set FLASK_DEBUG= 1 
# command to run the app -> python -m flask run
from flask import Flask,escape,render_template,url_for,flash,redirect, request, abort
from gen_app.forms import RegNumForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'


@app.route('/home',methods=['GET','POST'])
def home():
        form = RegNumForm()
        if form.validate_on_submit():
            flash(f'{form.reg_num.data}','success')
            return redirect(url_for('info'))
        return render_template('home.html',title='home',form=form)


@app.route('/info',methods=['GET','POST'])
def info():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
