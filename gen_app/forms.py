from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,RadioField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from gen_app.models import User



# info page roll number form
class RollNumForm(FlaskForm):
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Check')

# info page main file upload form
class UploadForm(FlaskForm):
    uploaded_file = FileField('Upload File',validators=[DataRequired()])
    submit = SubmitField('Submit')

# info page append file form
class AppendFile(FlaskForm):
    append_file = FileField('Upload Append File',validators=[DataRequired()])
    submit = SubmitField('Submit')

# registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    # checking if same name exists or not
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username Already taken!')
    # checking if same email-id exists or not
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

class TcManualForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    father_name = StringField('Father Name', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    date_of_admission =  StringField('Date of Admission')
    Name_of_course_and_branch = StringField('Course and Branch', validators=[DataRequired()])
    Year_and_month_of_passing = StringField('Year and month of passing')
    community = StringField('Community', validators=[DataRequired()])
    promotion = RadioField('Promotion', choices = ['Yes','No'],default='Yes')
    conduct =  StringField('Conduct',default='Satisfactory')
    identification =  StringField('Identification')
    identification_1 =  StringField('Identification')
    general_remarks =  StringField('General Remarks')
    submit = SubmitField('Submit')

class ConductManualForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    father_name = StringField('Father Name', validators=[DataRequired()])
    Name_of_course_and_branch = StringField('Course and Branch', validators=[DataRequired()])
    academic_year = StringField('Academic Year')
    conduct =  StringField('Conduct',default='Satisfactory')
    submit = SubmitField('Submit')

class BonafideManualForm(FlaskForm):
    admission_number = StringField('Admission Number')
    bonafide_number = StringField('Bonafide Number')
    roll_num = StringField('Roll Number')
    student_name = StringField('Student Name')
    father_name = StringField('Father Name')
    academic_year = StringField('Academic Year')
    semester = StringField('Semester')
    reason = StringField('Reason')
    submit = SubmitField('Submit')