from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from numpy import nan
from gen_app.forms import RollNumForm, UploadForm , RegistrationForm, LoginForm, ManualForm, AppendFile
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
from gen_app import app,db, bcrypt
from gen_app.models import User,Issued
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import csv

# home route
@app.route('/')
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
        form = rollnumform()
        form2 = uploadfile()
        form3 = AppendFile()

        if form.validate_on_submit():
        rn = form.roll_num.data
        df = pd.read_csv('/gen_app/static/excel.csv')
        index = df.keys()                                       #getting the coulmn names
        index = list(index)                                     #turning it into list to make access easy 
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

    if form2.validate_on_submit():
        filepath = os.path.join(r'/gen_app/static','excel.csv')
        form2.uploaded_file.data.save(filepath)
        return redirect(url_for('home'))

    if form3.validate_on_submit():
        filepath = os.path.join(r'/gen_app/static','excel_append.csv')
        form3.append_file.data.save(filepath)
        dataframe = pd.read_csv('/gen_app/static/excel_append.csv')
        index = dataframe.keys()                                       
        index = list(index)
        dataframe = dataframe.values.tolist()
        return render_template('visual.html',title='Appended File', dataframe = dataframe, headings = index)

    return render_template('home.html',title='home',form=form,form2=form2,form3=form3)

@app.route("/append_file")
@login_required
def append_file():
    with open('/gen_app/static/excel_append.csv','r') as new_info:
        reader = csv.reader(new_info)
        with open('/gen_app/static/excel.csv','a', newline='', encoding='utf-8') as info:
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
    df = pd.read_csv('/gen_app/static/excel.csv')
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
    img  =  Image.open('/gen_app/static/TC.jpg')
    date_of_leaving = datetime.date.today()
    date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 21)    
    admission_no = int(w[2])
    roll_number = w[3]
    name = w[4]
    father_name = w[5]
    date_of_birth = w[6]
    community = w[7]
    date_of_admission = w[8]
    course_and_branch = w[9]
    promotion = w[11]
    month_pass = w[12]
    conduct = w[13]
    identification = w[14]
    general_remarks = w[15]
    academic_year = w[16]    
    draw.text(xy=(1300,426),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,470),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,514),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(1300,558),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(1300,602),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(1300,643),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(1300,722),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(1300,796),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(1300,840),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(1300,889),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(1320,932),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(1300,1008),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    draw.text(xy=(630,299),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(1695,335),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(650,362),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1716,370),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1057,370),text='{}'.format(admission_no),fill=(0,0,0), font = font)
    draw.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font)
    draw.text(xy=(280,445),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(420,489),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(420,533),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(420,577),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(420,621),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(420,662),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(420,741),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(420,815),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(420,859),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(420,908),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(551,951),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(420,1027),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    img.save(r'/gen_app/static/saved/TC.pdf')
    return send_file(r'/static/saved/TC.pdf',attachment_filename='TC.pdf')

# Return original TC route
@app.route('/return_tc_original/<string:rn>', methods=['GET'])
@login_required
def return_tc_original(rn):
    df = pd.read_csv('/gen_app/static/excel.csv')
    index = df.keys()                                       #getting the coulmn names
    index = list(index)                                        #turning it into list to make access easy 
    data = df[index[3]]                                     #passing the coulmn key name to the df and passing whole coulmn to data
    data = list(data)                                       #turning it into list for easy access
    idx = data.index(rn)                                  #idx gives the index of the roll number entered in the array and we use it to find row
    a = df.iloc[[idx]]                                        #using iloc to find one specific row which will later be found and passed fro the search function 
    q = a.values                                            #a is storing the data that is then turned into a np array which has all elements in one single element
    w = q[0]                                                #q was a arry of arry and now we turn w into a single array and use it 
    today = datetime.date.today()
    today = today.strftime('%d-%m-%Y')
    img  =  Image.open('/gen_app/static/TC.jpg')
    date_of_leaving = datetime.date.today()
    date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 21)    
    admission_no = int(w[2])
    roll_number = w[3]
    name = w[4]
    father_name = w[5]
    date_of_birth = w[6]
    community = w[7]
    date_of_admission = w[8]
    course_and_branch = w[9]
    promotion = w[11]
    month_pass = w[12]
    conduct = w[13]
    identification = w[14]
    general_remarks = w[15]
    academic_year = w[16]    
    draw.text(xy=(1300,426),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,470),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,514),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(1300,558),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(1300,602),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(1300,643),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(1300,722),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(1300,796),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(1300,840),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(1300,889),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(1320,932),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(1300,1008),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    draw.text(xy=(630,299),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(1695,335),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(650,362),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1716,370),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1057,370),text='{}'.format(admission_no),fill=(0,0,0), font = font)
    draw.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font)

    draw.text(xy=(280,445),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(420,489),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(420,533),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(420,577),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(420,621),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(420,662),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(420,741),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(420,815),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(420,859),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(420,908),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(551,951),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(420,1027),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    img.save(r'/gen_app/static/saved/TC.pdf')
    db_data = Issued.query.filter_by(roll_num=rn).first()
    if db_data:
        return send_file(r'/static/saved/TC.pdf',attachment_filename='TC.pdf')
    else:
        issue = Issued(roll_num = rn,author = current_user)
        db.session.add(issue)
        db.session.commit()
        return send_file(r'/static/saved/TC.pdf',attachment_filename='TC.pdf')

# return duplicate TC
@app.route('/return_tc_duplicate/<string:rn>', methods=['GET'])
@login_required
def return_tc_duplicate(rn):
    df = pd.read_csv('/gen_app/static/excel.csv')
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
    img  =  Image.open('/gen_app/static/TC_dup.jpg')
    date_of_leaving = datetime.date.today()
    date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 21)    
    admission_no = int(w[2])
    roll_number = w[3]
    name = w[4]
    father_name = w[5]
    date_of_birth = w[6]
    community = w[7]
    date_of_admission = w[8]
    course_and_branch = w[9]
    promotion = w[11]
    month_pass = w[12]
    conduct = w[13]
    identification = w[14]
    general_remarks = w[15]
    academic_year = w[16]    
    draw.text(xy=(1300,426),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,470),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(1300,514),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(1300,558),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(1300,602),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(1300,643),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(1300,722),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(1300,796),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(1300,840),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(1300,889),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(1320,932),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(1300,1008),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    draw.text(xy=(630,299),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(1695,335),text='{}'.format(today),fill=(0,0,0), font = font)
    draw.text(xy=(650,362),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1716,370),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw.text(xy=(1057,370),text='{}'.format(admission_no),fill=(0,0,0), font = font)
    draw.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font)

    draw.text(xy=(280,445),text='{}'.format(name),fill=(0,0,0), font = font)
    draw.text(xy=(420,489),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw.text(xy=(420,533),text='{}'.format(date_of_birth),fill=(0,0,0), font = font)
    draw.text(xy=(420,577),text='{}'.format(date_of_admission),fill=(0,0,0), font = font)
    draw.text(xy=(420,621),text='{}'.format(course_and_branch),fill=(0,0,0), font = font)
    draw.text(xy=(420,662),text='{}'.format(date_of_leaving),fill=(0,0,0), font = font)
    if promotion == nan:
        draw.text(xy=(420,741),text='{}'.format(promotion),fill=(0,0,0), font = font)
    draw.text(xy=(420,815),text='{}'.format(month_pass),fill=(0,0,0), font = font)
    draw.text(xy=(420,859),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw.text(xy=(420,908),text='{}'.format(community),fill=(0,0,0), font = font)
    draw.text(xy=(551,951),text='{}'.format(identification),fill=(0,0,0), font = font)
    draw.text(xy=(420,1027),text='{}'.format(general_remarks),fill=(0,0,0), font = font)
    img.save(r'/gen_app/static/saved/TC_dup.pdf') 
    return send_file(r'/static/saved/TC_dup.pdf',attachment_filename='TC_dup.pdf')


# conduct return route
@app.route('/return_conduct/<string:rn>', methods=['GET'])
@login_required
def return_conduct(rn):
    df = pd.read_csv('/gen_app/static/excel.csv')
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
    img  =  Image.open('/gen_app/static/TC.jpg')
    date_of_leaving = datetime.date.today()
    date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 21)    
    admission_no = int(w[2])
    roll_number = w[3]
    name = w[4]
    father_name = w[5]
    date_of_birth = w[6]
    community = w[7]
    date_of_admission = w[8]
    course_and_branch = w[9]
    promotion = w[11]
    month_pass = w[12]
    conduct = w[13]
    identification = w[14]
    general_remarks = w[15]
    academic_year = w[16] 
    img1  =  Image.open('/gen_app/static/conduct.jpg')
    draw1 = ImageDraw.Draw(img1)
    font = ImageFont.truetype("arial.ttf", 28)
    font1 = ImageFont.truetype("arial.ttf", 24)
    if len(name) >= 30:
        draw1.text(xy=(1380,610),text='{}'.format(name),fill=(0,0,0), font = font1)
    else:
        draw1.text(xy=(1380,605),text='{}'.format(name),fill=(0,0,0), font = font)
    if len(father_name) >= 26:
        draw1.text(xy=(1050,686),text='{}'.format(father_name),fill=(0,0,0), font = font1)
    else:
        draw1.text(xy=(1050,686),text='{}'.format(father_name),fill=(0,0,0), font = font)
    draw1.text(xy=(1620,686),text='{}'.format(roll_number),fill=(0,0,0), font = font)
    draw1.text(xy=(1465,770),text='{}'.format(course_and_branch),fill=(0,0,0), font = font1)
    draw1.text(xy=(1285,845),text='{}'.format(academic_year),fill=(0,0,0), font = font)
    draw1.text(xy=(1705,927),text='{}'.format(conduct),fill=(0,0,0), font = font)
    draw1.text(xy=(630,299),text='{}'.format(today),fill=(0,0,0), font = font1)
    draw1.text(xy=(1700,335),text='{}'.format(today),fill=(0,0,0), font = font1)
    draw1.text(xy=(655,362),text='{}'.format(roll_number),fill=(0,0,0), font = font1)
    draw1.text(xy=(1716,370),text='{}'.format(roll_number),fill=(0,0,0), font = font1)
    draw1.text(xy=(1057,370),text='{}'.format(admission_no),fill=(0,0,0), font = font1)
    draw1.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font1)
    draw1.text(xy=(185,660),text='{}'.format(name),fill=(0,0,0), font = font1)
    draw1.text(xy=(270,720),text='{}'.format(father_name),fill=(0,0,0), font = font1)
    draw1.text(xy=(272,785),text='{}'.format(roll_number),fill=(0,0,0), font = font1)
    draw1.text(xy=(375,846),text='{}'.format(course_and_branch),fill=(0,0,0), font = font1)
    draw1.text(xy=(440,905),text='{}'.format(academic_year),fill=(0,0,0), font = font1)
    draw1.text(xy=(338,1025),text='{}'.format(conduct),fill=(0,0,0), font = font1)
    img1.save(r'/gen_app/static/saved/conduct.pdf')
    return send_file(r'/static/saved/conduct.pdf',attachment_filename='conduct.pdf')


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

@app.route("/manual_generate",methods=['GET','POST'])
@login_required
def manual_generate():
    form = ManualForm()
    if form.validate_on_submit():
        # draw data here
        return render_template('info.html',title='Issued',form=form, rn=form.roll_num.data)
    return render_template('manual_generate.html',title='Issued',form=form)


@app.route("/edit_tc/<string:rn>",methods=['GET','POST'])
@login_required
def edit_tc(rn):
    form = ManualForm()
    if form.validate_on_submit():
        return render_template('info.html',title='Issued',rn=form.roll_num.data)
    elif request.method == 'GET':
        df = pd.read_csv('/gen_app/static/excel.csv')
        index = df.keys()                                       #getting the coulmn names
        index = list(index)                                     #turning it into list to make access easy 
        data = df[index[3]]                                     #passing the coulmn key name to the df and passing whole coulmn to data
        data = list(data)                                       #turning it into list for easy access
        idx = data.index(rn)                                    #idx gives the index of the roll number entered in the array and we use it to find row
        a = df.iloc[[idx]]                                      #using ilot to find one specific row which will later be found and passed fro the search function 
        q = a.values                                            #a is storing the data that is then turned into a np array which has all elements in one single element
        w = q[0]                                                #q was a arry of arry and now we turn w into a single array and use it 
        today = datetime.date.today()
        today = today.strftime('%d-%m-%Y')
        img  =  Image.open('/gen_app/static/TC.jpg')
        date_of_leaving = datetime.date.today()
        date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 21)    
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