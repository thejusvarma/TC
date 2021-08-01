from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from numpy import dtype
from gen_app.forms import rollnumform, uploadfile, RegistrationForm
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
import sys
from io import BytesIO
from werkzeug.utils import secure_filename
from gen_app import app,db, bcrypt
from gen_app.models import User,Issued
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home',methods=['GET','POST'])
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
            return render_template('info.html',title='Student Info',name=df[0])

        if form2.uploaded_file.data:
            # data = pd.read_excel(form2.uploaded_file)
            # filename = secure_filename(form2.uploaded_file.data['excel'].filename)
            filepath = os.path.join(r'gen_app\static','excel.csv')
            form2.uploaded_file.data.save(filepath)
            return render_template('home.html',title='home',form=form,form2=form2)

        return render_template('home.html',title='home',form2=form2,form=form)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
    
#         if form2.validate_on_submit():
#             # data = pd.read_excel(form2.uploaded_file)
#             filename = secure_filename(form2.uploaded_file.data)
#             filepath = os.path.join(r'gen_app\static',filename)
#             form2.uploaded_file.data.save(filepath)
#             print('This', file=sys.stderr)
#             return render_template('home.html',title='home',form=form,form2=form2)

@app.route('/return-file/', methods=['GET', 'POST'])
def file_download():
    return send_file(r'static\saved\TC.pdf',attachment_filename='TC.pdf')


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # making instance (form) of RegsitrationForm class made in forms.py
    form = RegistrationForm()
    # if content is validated then flashing message and updating data into database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Login Please','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)
 
