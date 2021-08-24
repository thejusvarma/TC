from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,RadioField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from gen_app.models import User
import pandas as pd


class RollNumForm(FlaskForm):
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Check')

class UploadForm(FlaskForm):
    uploaded_file = FileField('Upload File',validators=[DataRequired(),FileAllowed(['csv'])])
    submit = SubmitField('Submit')

class AppendFile(FlaskForm):
    append_file = FileField('Upload Append File',validators=[DataRequired(),FileAllowed(['csv'])])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already taken!')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('E-Mail Id already exists')

# creating login form properties
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ManualForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    father_name = StringField('Father Name', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    date_of_admission =  StringField('Date of Admission')
    Name_of_course_and_branch = StringField('Course and Branch', validators=[DataRequired()])
    Year_and_month_of_passing = StringField('Year and month of passing')
    community = StringField('Community', validators=[DataRequired()])
    promotion = RadioField('Promotion', choices = ['Yes', 'No'])
    conduct =  StringField('Conduct')
    identification =  StringField('Identification')
    identification_1 =  StringField('Identification')
    general_remarks =  StringField('General Remarks')
    submit = SubmitField('Submit')
