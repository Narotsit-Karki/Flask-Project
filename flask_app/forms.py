from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length,Email,EqualTo,ValidationError
from flask_app.models import Users

class Registration_Form(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=10)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('❗ Username is already taken!!. Enter a different username')

    def validate_email(self,email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('❗ Email already taken !! Enter a different email')

class Login_Form(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10)])
    remember_me = BooleanField('Remember Me') # for cookies
    submit = SubmitField('Log in')




class Update_Account_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update Profile Pic',validators=[FileAllowed(['jpg','png'])])
    update = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('❗ Username is already taken!!. Enter a different username')
    def validate_email(self,email):
        if email.data != current_user.email:
            email = Users.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('❗ Email already taken !! Enter a different email')

class Post_Form(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')


class Edit_Post_Form(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Update')