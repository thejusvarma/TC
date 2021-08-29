from flask import Flask,render_template,url_for,flash,redirect,request,send_file
from gen_app import app,db, bcrypt
from gen_app.models import User,Issued
from gen_app.functions import tc,tc_dup,conduct
import gen_app.handlers
from gen_app.forms import RollNumForm, UploadForm , RegistrationForm, LoginForm, ManualForm, AppendFile
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image,ImageFont,ImageDraw
from numpy import nan
import pandas as pd
import os
import datetime
import csv

# home route
@app.route('/')
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    form = RollNumForm()
    form2 = UploadForm()
    form3 = AppendFile()
    # first form - roll number form
    if form.validate_on_submit():
        rn = form.roll_num.data    
        df = pd.read_csv('gen_app/static/excel.csv')
        index = df.keys()                                       #getting the coulmn names
        index = list(index)                                        #turning it into list to make access easy 
        data = df[index[3]]                                     #passing the coulmn key name to the df and passing whole coulmn to data
        data = list(data)                                       #turning it into list for easy access
        if rn in data:
            db_data1 = Issued.query.filter_by(roll_num=rn).first()
            db_data2 = None
            if db_data1:
                db_data2 = User.query.filter_by(id=db_data1.user_id).first()
                if db_data2:
                    flash(f"TC already Issued to {rn} on {db_data1.date_posted.strftime('%d-%m-%Y')} ",'danger')
                    return render_template('info.html',title='Student Info',rn=rn)
            return render_template('info.html',title='Student Info',rn=rn)
        else:
            flash(f'Invalid Roll Number','danger')
            return redirect(url_for('home'))

    # second form - uploading main csv file
    if form2.validate_on_submit():
        filepath = os.path.join(r'gen_app/static','excel.csv')
        form2.uploaded_file.data.save(filepath)
        return redirect(url_for('home'))

    # third form - append file 
    if form3.validate_on_submit():
        filepath = os.path.join(r'gen_app/static','excel_append.csv')
        form3.append_file.data.save(filepath)
        dataframe = pd.read_csv('gen_app/static/excel_append.csv')
        index = dataframe.keys()                                       
        index = list(index)
        dataframe = dataframe.values.tolist()
        return render_template('visual.html',title='Appended File', dataframe = dataframe, headings = index)

    return render_template('home.html',title='home',form=form,form2=form2,form3=form3)

# append file route
@app.route("/append_file")
@login_required
def append_file():
    with open('gen_app/static/excel_append.csv','r') as new_info:
        reader = csv.reader(new_info)
        with open('gen_app/static/excel.csv','a', newline='', encoding='utf-8') as info:
            append = csv.writer(info)
            next(reader)
            for i in reader:
                append.writerow(i)
    flash(f'Successfully Added','success')
    return redirect(url_for('home'))

# TC preview route
@app.route('/return_tc_preview/<string:rn>', methods=['GET'])
@login_required
def return_tc_preview(rn):
    tc(rn)
    return send_file(r'static/saved/TC.pdf',attachment_filename='TC.pdf')

# Return original TC route
@app.route('/return_tc_original/<string:rn>', methods=['GET'])
@login_required
def return_tc_original(rn):
    tc(rn)
    db_data = Issued.query.filter_by(roll_num=rn).first()
    db_data1 = Issued.query.order_by(Issued.id.desc()).first()
    if db_data:
        return send_file(r'static/saved/TC.pdf',attachment_filename='TC.pdf')
    else:
        if db_data1:
            issue = Issued(roll_num = rn,tc_num = (db_data1.tc_num)+1,author = current_user)
            db.session.add(issue)
            db.session.commit()
            return send_file(r'static/saved/TC.pdf',attachment_filename='TC.pdf')
        else:
            issue = Issued(roll_num = rn,tc_num = 8401,author = current_user)
            db.session.add(issue)
            db.session.commit()
            return send_file(r'static/saved/TC.pdf',attachment_filename='TC.pdf')
            


# return duplicate TC
@app.route('/return_tc_duplicate/<string:rn>', methods=['GET'])
@login_required
def return_tc_duplicate(rn):
    tc_dup(rn)
    return send_file(r'static/saved/TC_dup.pdf',attachment_filename='TC_dup.pdf')


# conduct return route
@app.route('/return_conduct/<string:rn>', methods=['GET'])
@login_required
def return_conduct(rn):
    conduct(rn)
    return send_file(r'static/saved/conduct.pdf',attachment_filename='conduct.pdf')


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
@login_required
def issued():
    data = Issued.query.filter_by(user_id=current_user.id).all()
    return render_template('issue.html',title='Issued',datas=data)

# manual Tc generation
@app.route("/manual_generate",methods=['GET','POST'])
@login_required
def manual_generate():
    form = ManualForm()
    if form.validate_on_submit():
        # draw data here
        today = datetime.date.today()
        today = today.strftime('%d-%m-%Y')
        img  =  Image.open('gen_app/static/TC.jpg')
        date_of_leaving = datetime.date.today()
        date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype("arial.ttf", 21)    
        font = ImageFont.load_default()
        admission_no = form.admission_number.data
        roll_number = form.roll_num.data
        name = form.student_name.data
        father_name = form.father_name.data
        date_of_birth = form.date_of_birth.data
        community = form.community.data
        date_of_admission =form.date_of_admission.data
        course_and_branch = form.Name_of_course_and_branch.data
        promotion = form.promotion.data
        month_pass = form.Year_and_month_of_passing.data
        conduct = form.conduct.data
        identification = form.identification.data
        identification_1 = form.identification_1.data
        general_remarks = form.general_remarks.data
        # font1 = ImageFont.truetype("arial.ttf", 18)    
        font1 = ImageFont.load_default()

        # getting tc_number
        db_data1 = Issued.query.order_by(Issued.id.desc()).first()
        if db_data1:
            tc_num = (db_data1.tc_num)+1
        else:
            tc_num = 8401

        draw.text(xy=(968,335),text='{}'.format(tc_num),fill=(0,0,0), font = font) 
        draw.text(xy=(1300,426),text='{}'.format(name),fill=(0,0,0), font = font)
        draw.text(xy=(1300,470),text='{}'.format(father_name),fill=(0,0,0), font = font)
        draw.text(xy=(1300,514),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
        draw.text(xy=(1300,558),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
        draw.text(xy=(1300,602),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
        draw.text(xy=(1300,643),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
        
        draw.text(xy=(1300,722),text='{}'.format(promotion),fill=(0,0,0), font = font)
        draw.text(xy=(1300,796),text='{}'.format(month_pass),fill=(0,0,0), font = font)
        draw.text(xy=(1300,840),text='{}'.format(conduct),fill=(0,0,0), font = font)
        draw.text(xy=(1300,889),text='{}'.format(community),fill=(0,0,0), font = font)
        draw.text(xy=(1300,932),text='{}'.format(identification),fill=(0,0,0), font = font)
        draw.text(xy=(1300,964),text='{}'.format(identification_1),fill=(0,0,0), font = font)
        draw.text(xy=(1300,1008),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
        draw.text(xy=(630,299),text='{}'.format(today),fill=(0,0,0), font = font)
        draw.text(xy=(1775,335),text='{}'.format(today),fill=(0,0,0), font = font)
        draw.text(xy=(650,362),text='{}'.format(roll_number),fill=(0,0,0), font = font)
        draw.text(xy=(1786,370),text='{}'.format(roll_number),fill=(0,0,0), font = font)
        draw.text(xy=(1057,370),text='{}'.format(admission_no),fill=(0,0,0), font = font)
        draw.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font)
        draw.text(xy=(250,299),text='{}'.format(tc_num),fill=(0,0,0), font = font) 
        draw.text(xy=(280,445),text='{}'.format(name),fill=(0,0,0), font = font)
        draw.text(xy=(420,489),text='{}'.format(father_name),fill=(0,0,0), font = font)
        draw.text(xy=(420,533),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
        draw.text(xy=(420,577),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
        draw.text(xy=(420,621),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
        draw.text(xy=(420,662),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
        
        draw.text(xy=(420,741),text='{}'.format(promotion),fill=(0,0,0), font = font)
        draw.text(xy=(420,815),text='{}'.format(month_pass),fill=(0,0,0), font = font)
        draw.text(xy=(420,859),text='{}'.format(conduct),fill=(0,0,0), font = font)
        draw.text(xy=(420,908),text='{}'.format(community),fill=(0,0,0), font = font)
        draw.text(xy=(551,951),text='{}'.format(identification),fill=(0,0,0), font = font1)
        draw.text(xy=(551,983),text='{}'.format(identification_1),fill=(0,0,0), font = font1)
        draw.text(xy=(420,1027),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
        img.save(r'gen_app/static/saved/TC.pdf')
        return send_file(r'static/saved/TC.pdf',attachment_filename='TC.pdf')
    return render_template('manual_generate.html',title='Issued',form=form)


@app.route("/edit_tc/<string:rn>",methods=['GET','POST'])
@login_required
def edit_tc(rn):
    form = ManualForm()
    if form.validate_on_submit():
        return render_template('info.html',title='Issued',rn=form.roll_num.data)
    elif request.method == 'GET':
        df = pd.read_csv('gen_app/static/excel.csv')
        index = df.keys()                                       #getting the coulmn names
        index = list(index)                                        #turning it into list to make access easy 
        data = df[index[3]]                                     #passing the coulmn key name to the df and passing whole coulmn to data
        data = list(data)                                       #turning it into list for easy access
        idx = data.index(rn)                                  #idx gives the index of the roll number entered in the array and we use it to find row
        a = df.iloc[[idx]]                                        #using ilot to find one specific row which will later be found and passed fro the search function 
        q = a.values                                            #a is storing the data that is then turned into a np array which has all elements in one single element
        w = q[0]                                                #q was a arry of arry and now we turn w into a single array and use it 
        today = datetime.date.today()
        today = today.strftime('%d-%m-%Y')
        img  =  Image.open('gen_app/static/TC.jpg')
        date_of_leaving = datetime.date.today()
        date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype("arial.ttf", 21)
        font = ImageFont.load_default()    
        form.admission_number.data = int(w[2])
        form.roll_num.data = w[3]
        form.student_name.data = w[4]
        form.father_name.data = w[5]
        form.date_of_birth.data = w[6]
        form.community.data = w[7]
        form.date_of_admission.data = w[8]
        form.Name_of_course_and_branch.data = w[9]
        form.Year_and_month_of_passing.data = w[12]
        form.conduct.data = w[13]
        return render_template('manual_generate.html',title='Issued',form=form,rn=form.roll_num)
    return render_template('manual_generate.html',title='Issued',form=form)
