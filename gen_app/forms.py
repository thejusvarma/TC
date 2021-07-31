from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError

class rollnumform(FlaskForm):
    roll_num = StringField('Roll Number', validators=[DataRequired()])
    submit = SubmitField('Check')
    # def validate_username(self,username):
    #     user = User.query.filter_by(username = username.data).first()
    #     if user:
    #         raise ValidationError('Username Already taken!')

    # def validate_email(self,email):
    #     user = User.query.filter_by(email = email.data).first()
    #     if user:
    #         raise ValidationError('E-Mail Id already exists')
class uploadfile(FlaskForm):
    uploaded_file = FileField('Upload File',validators=[DataRequired(),FileAllowed(['xlsx'])])
    submit = SubmitField('Submit')