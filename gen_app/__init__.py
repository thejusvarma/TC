from flask import Flask, send_file,escape,render_template,url_for,flash,redirect, request, abort,send_file, send_from_directory, safe_join
from gen_app.forms import RegNumForm
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
        form = RegNumForm()
        if form.validate_on_submit():
            df = ["thejus", "shivarmpally", "btech"]
            img  =  Image.open('gen_app\static\TC.jpg')
            draw = ImageDraw.Draw(img)
            draw.text(xy=(200,200),text= '{}'.format(df[0]),fill=(0,0,0))
            img.save(r'gen_app\static\saved\{}.pdf'.format(df[0]))
            
            return render_template('info.html',title='Student Info',name=df[0])
        return render_template('home.html',title='home',form=form)

@app.route('/return-file/', methods=['GET', 'POST'])
def file_download():
    return send_file(r'static\saved\thejus.pdf',attachment_filename='thejus.pdf')
