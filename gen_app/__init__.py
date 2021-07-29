from flask import Flask,escape,render_template,url_for,flash,redirect, request, abort
from gen_app.forms import RegNumForm
from PIL import Image,ImageFont,ImageDraw
import pandas as pd
import os
import sys
from pathlib import Path


app = Flask(__name__)
app.config['SECRET_KEY'] = '48c92cc12c8608d0ae64d2615acf501a'


@app.route('/home',methods=['GET','POST'])
def home():
        form = RegNumForm()
        if form.validate_on_submit():
            
            # df = form.reg_num.data
            # print(df, file=sys.stderr)
            df = ["thejus", "shivarmpally", "btech"]
            img  =  Image.open('gen_app\static\sample.jpg')
            draw = ImageDraw.Draw(img)
           
            draw.text(xy=(200,200),text= '{}'.format(df[0]),fill=(0,0,0))
            img.save(r'Downloads\{}.jpg'.format(df[0]))

            return render_template('info.html',title='Student Info' )
        return render_template('home.html',title='home',form=form)
