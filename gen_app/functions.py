from flask import Flask,render_template,url_for,flash,redirect,request,send_file
from gen_app import app,db
from gen_app.models import User,Issued
import gen_app.handlers
from PIL import Image,ImageFont,ImageDraw
from numpy import nan
import pandas as pd
import csv
import os
import datetime
from pathlib import Path

# preview and original tc generation function
def tc(rn):
    my_file = Path('gen_app/static/excel.csv')
    if my_file.is_file():
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
        # font = ImageFont.load_default()
        font = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 21)
        admission_no = int(w[2])
        roll_number = w[3]
        name = w[4]
        father_name = w[5]
        date_of_birth = w[6]
        community = w[7]
        date_of_admission = w[8]
        course_and_branch = w[9]
        # promotion = w[11]
        promotion = "Yes"
        month_pass = w[12]
        conduct = w[13]
        identification = w[14]
        identification_1 = w[15]
        general_remarks = w[16]
        academic_year = w[17]
        # font1 = ImageFont.truetype("arial.ttf", 18)    
        # font1 = ImageFont.load_default()
        font1 = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 18)

        # getting tc_number
        db_data1 = Issued.query.order_by(Issued.id.desc()).first() 
        db_data2 = Issued.query.filter_by(roll_num=rn).first()
        if db_data1:
            tc_num = (db_data1.tc_num)+1
            if db_data2:
                tc_num = db_data2.tc_num
        else:
            tc_num = 8401

        # drawing on the original tc image
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
        draw.text(xy=(243,299),text='{}'.format(tc_num),fill=(0,0,0), font = font)
        draw.text(xy=(325,362),text='{}'.format(admission_no),fill=(0,0,0), font = font)
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
    else:
        return render_template('errors/excel.html')

# duplicate tc generation function
def tc_dup(rn):
    my_file = Path('gen_app/static/excel.csv')
    if my_file.is_file():
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
        img  =  Image.open('gen_app/static/TC_dup.jpg')
        date_of_leaving = datetime.date.today()
        date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype("arial.ttf", 21)
        # font = ImageFont.load_default()    
        font = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 21)
        admission_no = int(w[2])
        roll_number = w[3]
        name = w[4]
        father_name = w[5]
        date_of_birth = w[6]
        community = w[7]
        date_of_admission = w[8]
        course_and_branch = w[9]
        # promotion = w[11]
        promotion = "Yes"
        month_pass = w[12]
        conduct = w[13]
        identification = w[14]
        identification_1 = w[15]
        general_remarks = w[16]
        academic_year = w[17]    
        # font1 = ImageFont.truetype("arial.ttf", 18)
        # font1 = ImageFont.load_default()
        font1 = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 18)

        # getting tc_number
        db_data1 = Issued.query.order_by(Issued.id.desc()).first()
        db_data2 = Issued.query.filter_by(roll_num=rn).first()
        if db_data1:
            tc_num = (db_data1.tc_num)+1
            if db_data2:
                tc_num = db_data2.tc_num
        else:
            tc_num = 8401
        # drawing one the duplicate TC image
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
        draw.text(xy=(243,299),text='{}'.format(tc_num),fill=(0,0,0), font = font)
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
        img.save(r'gen_app/static/saved/TC_dup.pdf') 
    else:
        return render_template('errors/excel.html')

# conduct generation function
def conduct(rn):
    my_file = Path('gen_app/static/excel.csv')
    if my_file.is_file():
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
        admission_no = int(w[2])
        roll_number = w[3]
        name = w[4]
        father_name = w[5]
        course_and_branch = w[9]
        conduct = w[13]
        academic_year = w[17] 
        img1  =  Image.open('gen_app/static/conduct.jpg')
        draw1 = ImageDraw.Draw(img1)
        # font = ImageFont.truetype("arial.ttf", 28)
        # font = ImageFont.load_default()
        font = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 28)
        # font1 = ImageFont.truetype("arial.ttf", 24)
        # font1 = ImageFont.load_default()
        font1 = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 24)
        # drawing on the conduct image
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
        img1.save(r'gen_app/static/saved/conduct.pdf')
    else:
            return render_template('errors/404.html')

# manual tc generation fucntion
def manual_gen(form):
    today = datetime.date.today()
    today = today.strftime('%d-%m-%Y')
    img  =  Image.open('gen_app/static/TC.jpg')
    date_of_leaving = datetime.date.today()
    date_of_leaving = date_of_leaving.strftime('%d-%m-%Y')
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype("arial.ttf", 21)    
    # font = ImageFont.load_default()
    font = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 21)

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
    font1 = ImageFont.truetype('gen_app/static/Fonts/arial.ttf', 18)
    # getting next tc_number
    db_data1 = Issued.query.order_by(Issued.id.desc()).first()
    db_data2 = Issued.query.filter_by(roll_num=roll_number).first()
    if db_data1:
        tc_num = (db_data1.tc_num)+1
        if db_data2:
            tc_num = db_data2.tc_num
        else:
            tc_num = 8401
    # drawing on tc image
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
