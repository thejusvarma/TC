from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from gen_app.forms import rollnumform, uploadfile
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
from io import BytesIO
import sys
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'


@app.route('/home',methods=['GET','POST'])
def home():
        form = rollnumform()
        form2 = uploadfile()

        if form.roll_num.data:
            rn = form.roll_num.data
            df = pd.read_excel('gen_app\static\excel.xlsx')
            print(df)
            # data = df[df['Conduct'] == 'Satisfactory']
            # print(data)
            df = ['thej','dffd']
            img  =  Image.open('gen_app\static\TC.jpg')
            draw = ImageDraw.Draw(img)
            draw.text(xy=(200,200),text='{}'.format(df[0]),fill=(0,0,0))
            img.save(r'gen_app\static\saved\{}.pdf'.format(df[0]))
            return render_template('info.html',title='Student Info',name=df[0])

        if form2.uploaded_file.data:
            # data = pd.read_excel(form2.uploaded_file)
            # filename = secure_filename(form2.uploaded_file.data['excel'].filename)
            filepath = os.path.join(r'gen_app\static','excel.xlsx')
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
    return send_file(r'static\saved\thejus.pdf',attachment_filename='thejus.pdf')