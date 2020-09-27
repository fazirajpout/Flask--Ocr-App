from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo,ValidationError
from ocrapp.models import User

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators = [DataRequired() ,Length(max = 10, min=2)])
    secondName = StringField('Second Name', validators = [DataRequired() ,Length(max = 10, min=2)])
    date=DateField('Date Of Birth')
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')
    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user:
           raise ValidationError('Already have an account for given email address!! please try with diffrent ')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit=SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    firstName = StringField('First Name', validators = [DataRequired() ,Length(max = 10, min=2)])
    secondName = StringField('Second Name', validators = [DataRequired() ,Length(max = 10, min=2)])
    date=DateField('Date Of Birth')
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit=SubmitField('Update')
    def validate_email(self,firstName,SecondName):
        if firstname != current_user.firstname and secondName != current_user.secondName:
             user= User.query.filter_by(firstName=FirstName.data,secondName=secondName.data).first()
             if user:
                 raise ValidationError('Already have an account for given email address!! please try with diffrent ')
    def validate_email(self,email):
            if email != current_user.email:
                 user= User.query.filter_by(email=email.data).first()
                 if user:
                      raise ValidationError('Already have an account for given email address!! please try with diffrent ')

class RequestResetForm(FlaskForm):
       email = StringField('Email', validators = [DataRequired(), Email()])
       submit=SubmitField('Request Password Reset')
       def validate_email(self,email):
           user= User.query.filter_by(email=email.data).first()
           if user is None:
               raise ValidationError('There is no account for that email.You must register first')
           


class ResetPasswordForm(FlaskForm):
     password = PasswordField('Password', validators = [DataRequired()])
     confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password')])
     submit=SubmitField('Reset Password')
