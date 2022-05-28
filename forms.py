from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length,Email,EqualTo

class Registration_Form(FlaskForm):
    username = StringField('Username',validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign Up')

class Login_Form(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10)])
    remember_me = BooleanField('Remember Me') # for cookies
    submit = SubmitField('Log in')


