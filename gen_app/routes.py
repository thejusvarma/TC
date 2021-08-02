from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from numpy import dtype
from gen_app.forms import rollnumform, uploadfile, RegistrationForm, LoginForm
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
import sys
from io import BytesIO
from werkzeug.utils import secure_filename
from gen_app import app,db, bcrypt
from gen_app.models import User,Issued
from flask_login import login_user, current_user, logout_user, login_required

access = ['thejusvarma11@gmail.com']

@app.route('/')
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
        
        form = rollnumform()
        form2 = uploadfile()

        if form.roll_num.data:
            rn = form.roll_num.data
            # df = pd.read_csv('gen_app\static\excel.csv')
            # data = df.loc('Team',dtype="object")
            # print(data)
            df = ['thej','dffd']
            img  =  Image.open('gen_app\static\TC.jpg')
            draw = ImageDraw.Draw(img)
            draw.text(xy=(200,200),text='{}'.format(df[0]),fill=(0,0,0))
            img.save(r'gen_app\static\saved\{}.pdf'.format('TC'))

            data = Issued.query.filter_by(roll_num=rn).first()
            data2 = None
            if data:
                data2 = User.query.filter_by(id=data.user_id).first()
            if data2:
                flash(f'TC already Issued by ','danger')

            return render_template('info.html',title='Student Info',rn=rn)

        if form2.uploaded_file.data:
            # data = pd.read_excel(form2.uploaded_file)
            # filename = secure_filename(form2.uploaded_file.data['excel'].filename)
            filepath = os.path.join(r'gen_app\static','excel.csv')
            form2.uploaded_file.data.save(filepath)
            return render_template('home.html',title='home',form=form,form2=form2)

        return render_template('home.html',title='home',form2=form2,form=form)


@app.route('/return_tc/<string:rn>', methods=['GET','POST'])
def return_tc(rn):
    issue = Issued(roll_num = rn,author = current_user)
    db.session.add(issue)
    db.session.commit()
    return send_file(r'static\saved\TC.pdf',attachment_filename='TC.pdf')

@app.route('/return_conduct/<string:rn>', methods=['GET','POST'])
def return_conduct(rn):
    data = Issued.query.filter_by(roll_num=rn).first()
    # issue = Issued(roll_num = rn,author = current_user)
    # db.session.add(issue)
    # db.session.commit()
    # if data:
    #     flash(f'TC already Issued','danger')
    return send_file(r'static\saved\TC.pdf',attachment_filename='TC.pdf')

@app.route("/register",methods=['GET','POST'])
@login_required
def register():     
    # making instance (form) of RegsitrationForm class made in forms.py
    form = RegistrationForm()

    # if content is validated then flashing message and updating data into database
    if form.validate_on_submit():
        access.append(form.email.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Login Please','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)
 
# login route
@app.route("/login",methods=['GET','POST'])
def login():
    # checking user already logged in then he will be redirected to home route 
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # making instance (form) of LoginForm class made in forms.py
    form = LoginForm()

    # checking if form is valid or not
    if form.validate_on_submit():
        # creating user variable
        user = User.query.filter_by(email=form.email.data).first()
        # upon log in if such user exists AND the password matches then login granted
        
        if user and user.email in access and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'Login successfull!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessfull! Please check your E-mail and password ','danger')
            
    return render_template('login.html',title='Login',form=form)
 
# logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
