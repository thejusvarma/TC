from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from numpy import nan
from gen_app.forms import rollnumform, uploadfile, RegistrationForm, LoginForm, ManualForm
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
from gen_app import app,db, bcrypt
from gen_app.models import User,Issued
from flask_login import login_user, current_user, logout_user, login_required
import datetime

# home route
@app.route('/')
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
        form = rollnumform()
        form2 = uploadfile()

        if form.validate_on_submit():
            rn = form.roll_num.data
            db_data1 = Issued.query.filter_by(roll_num=rn).first()
            db_data2 = None
            if db_data1:
                db_data2 = User.query.filter_by(id=db_data1.user_id).first()
            if db_data2:
                flash(f"TC already Issued on {db_data1.date_posted.strftime('%d-%m-%Y')} by {db_data2.username}",'danger')

            df = pd.read_csv('gen_app\static\excel.csv')
            index = df.keys()                                       #getting the coulmn names
            index = list(index)                                        #turning it into list to make access easy 
            data = df[index[3]]                                     #passing the coulmn key name to the df and passing whole coulmn to data
            data = list(data)                                       #turning it into list for easy access
            if rn in data:
                idx = data.index(rn)                                  #idx gives the index of the roll number entered in the array and we use it to find row
                a = df.iloc[[idx]]                                        #using ilot to find one specific row which will later be found and passed fro the search function 
                q = a.values                                            #a is storing the data that is then turned into a np array which has all elements in one single element
                w = q[0]                                                #q was a arry of arry and now we turn w into a single array and use it 
                dob = str(w[6])                                         #taking the dob from the file in the date-month-year format 
                objDate = datetime.datetime.strptime(dob, '%d-%m-%Y').date()    
                r = objDate.strftime('%d %B %Y')
                w[6] = r
                today = datetime.date.today()
                if db_data1:
                    img  =  Image.open('gen_app\static\TC_dup.jpg')
                else:
                    img  =  Image.open('gen_app\static\TC.jpg')
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("arial.ttf", 23)
                font1 = ImageFont.truetype("arial.ttf", 16)
                draw.text(xy=(912,336),text='{}'.format(w[2]),fill=(0,0,0), font = font)
                draw.text(xy=(1740,296),text='{}'.format(today),fill=(0,0,0), font = font)
                draw.text(xy=(1694,336),text='{}'.format(w[3]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,392),text='{}'.format(w[4]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,436),text='{}'.format(w[5]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,480),text='{}'.format(w[6]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,521),text='{}'.format(w[8]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,565),text='{}'.format(w[9]),fill=(0,0,0), font = font)
                if w[12] != nan:
                    draw.text(xy=(1140,758),text='{}'.format(w[12]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,800),text='{}'.format(w[13]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,848),text='{}'.format(w[7]),fill=(0,0,0), font = font)
                draw.text(xy=(1240,891),text='{}'.format(w[14]),fill=(0,0,0), font = font)
                draw.text(xy=(1140,966),text='{}'.format(w[15]),fill=(0,0,0), font = font)
                
                draw.text(xy=(172,316),text='{}'.format(w[2]),fill=(0,0,0), font = font1)
                draw.text(xy=(566,254),text='{}'.format(today),fill=(0,0,0), font = font1)
                draw.text(xy=(508,316),text='{}'.format(w[3]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,397),text='{}'.format(w[4]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,441),text='{}'.format(w[5]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,485),text='{}'.format(w[6]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,526),text='{}'.format(w[8]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,570),text='{}'.format(w[9]),fill=(0,0,0), font = font1)
                if w[12] != nan:
                    draw.text(xy=(265,763),text='{}'.format(w[12]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,805),text='{}'.format(w[13]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,853),text='{}'.format(w[7]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,896),text='{}'.format(w[14]),fill=(0,0,0), font = font1)
                draw.text(xy=(265,971),text='{}'.format(w[15]),fill=(0,0,0), font = font1)
                img.save(r'gen_app\static\saved\TC.pdf')

                
                img1  =  Image.open('gen_app\static\conduct.jpg')
                draw1 = ImageDraw.Draw(img1)
                font = ImageFont.truetype("arial.ttf", 23)
                font1 = ImageFont.truetype("arial.ttf", 16)
                draw1.text(xy=(1090,542),text='{}'.format(w[4]),fill=(0,0,0), font = font)
                draw1.text(xy=(365,505),text='{}'.format(w[4]),fill=(0,0,0), font = font)
                draw1.text(xy=(863,650),text='{}'.format(w[3]),fill=(0,0,0), font = font)
                draw1.text(xy=(1694,336),text='{}'.format(w[3]),fill=(0,0,0), font = font)
                draw1.text(xy=(509,312),text='{}'.format(w[3]),fill=(0,0,0), font = font)
                draw1.text(xy=(138,621),text='{}'.format(w[3]),fill=(0,0,0), font = font)
                draw1.text(xy=(127,659),text='{}'.format(w[5]),fill=(0,0,0), font = font)
                draw1.text(xy=(1238,650),text='{}'.format(w[5]),fill=(0,0,0), font = font)
                draw1.text(xy=(44,775),text='{}'.format(w[9]),fill=(0,0,0), font = font)
                draw1.text(xy=(1246,758),text='{}'.format(w[9]),fill=(0,0,0), font = font)
                draw1.text(xy=(995,866),text='{}'.format(w[16]),fill=(0,0,0), font = font)
                draw1.text(xy=(70,853),text='{}'.format(w[16]),fill=(0,0,0), font = font)
                draw1.text(xy=(217,969),text='{}'.format(w[13]),fill=(0,0,0), font = font)
                draw1.text(xy=(900,972),text='{}'.format(w[13]),fill=(0,0,0), font = font)
                draw1.text(xy=(172,311),text='{}'.format(w[2]),fill=(0,0,0), font = font)
                draw1.text(xy=(912,336),text='{}'.format(w[2]),fill=(0,0,0), font = font)
                draw1.text(xy=(1740,296),text='{}'.format(today),fill=(0,0,0), font = font)
                draw1.text(xy=(566,249),text='{}'.format(today),fill=(0,0,0), font = font1)
                img1.save(r'gen_app\static\saved\conduct.pdf')
                return render_template('info.html',title='Student Info',rn=rn)
            else:
                flash(f'Invalid Roll Number','danger')
                return render_template('info.html',title='Student Info',rn=False)

        if form2.uploaded_file.data:
            filepath = os.path.join(r'gen_app\static','excel.csv')
            form2.uploaded_file.data.save(filepath)
            return render_template('home.html',title='home',form=form,form2=form2)

        return render_template('home.html',title='home',form2=form2,form=form)

# TC return route
@app.route('/return_tc/<string:rn>', methods=['GET'])
def return_tc(rn):
    db_data1 = Issued.query.filter_by(roll_num=rn).first()
    if db_data1:
        return send_file(r'static\saved\TC.pdf',attachment_filename='TC.pdf')
    else:
        issue = Issued(roll_num = rn,author = current_user)
        db.session.add(issue)
        db.session.commit()
        return send_file(r'static\saved\TC.pdf',attachment_filename='TC.pdf')

# conduct return route
@app.route('/return_conduct/<string:rn>', methods=['GET'])
def return_conduct(rn):
    return send_file(r'static\saved\conduct.pdf',attachment_filename='conduct.pdf')

# register route
@app.route("/register",methods=['GET','POST'])
@login_required
def register():
    # making instance (form) of RegsitrationForm class made in forms.py
    form = RegistrationForm()
    # if content is validated then flashing message and updating data into database
    if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created!','success')
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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

@app.route("/issued")
def issued():
    data = Issued.query.filter_by(user_id=current_user.id).all()
    return render_template('issue.html',title='Issued',datas=data)

@app.route("/manual_generate")
def manual_generate():
    form = ManualForm()
    return render_template('manual_generate.html',title='Issued',form=form)