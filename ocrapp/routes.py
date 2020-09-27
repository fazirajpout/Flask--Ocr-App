from flask import render_template,url_for,flash, redirect,request #flash is use for showing success and warning msgs
from ocrapp import app, db, bcrypt
from ocrapp.forms import RegistrationForm,LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from ocrapp.models import User
from flask_login import login_user,current_user,logout_user,login_required
import os
import pytesseract
import cv2
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from datetime import date
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisismysecret!')
app_root=os.path.dirname(os.path.abspath(__file__))
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\rmfaizan\Desktop\flask_blog\flaskblog\Tesseract-OCR\tesseract.exe"
posts= [
    {
        'author' : 'faizan',
         'title' : 'blog_Post 1',
         'content' :'first post content',
         'date_posted' :'29 july 2019'
        },
    {
        'author' : 'ali',
         'title' : 'blog_Post 2',
         'content' :'2nd post content',
         'date_posted' :'30 july 2019'
        }
    ]

@app.route('/')
def layout():
    return render_template("layout.html")
@app.route('/home')
@login_required
def home():
     return render_template("uploads.html")
@app.route('/uploads',methods = ['POST'])
@login_required
def uploads():
     target=os.path.join(app_root,'images/')
     print(target)

     if not os.path.isdir(target):
          os.mkdir(target)
     for file in request.files.getlist("file"):
          print(file)
          filename=file.filename
          destination="/".join([target,filename])
          print(destination)
          file.save(destination)
          img=cv2.imread(destination)
          data=pytesseract.image_to_string(img)
     return render_template("uploads.html",data=data)
@app.route('/about')
def about():
    return render_template('about.html', title = 'About')
@app.route('/register', methods = ['GET','POST']) #methods of accepeting requesting
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user= User(firstName=form.firstName.data, secondName = form.secondName.data, date=form.date.data, email = form.email.data, password=hashed_password)
         email = form.email.data
         token = s.dumps(email, salt='email-confirm')
         msg = Message('Confirm Email', sender='rajpoutfazi@gmail.com', recipients=[email])
         link = url_for('confirm_email', token=token, _external=True)
         msg.body = 'Your link is {}'.format(link)
         mail.send(msg)
         db.session.add(user)
         db.session.commit()
         flash(f'Now Please confirm your email address!!','success') #showing success msg if user created account successfuly
         #return redirect(url_for('login'))
         return render_template('register.html', title = 'Register' , form = form)
    return render_template('register.html', title = 'Register' , form = form)
@app.route('/login', methods = ['GET','POST'])
def login():
     if current_user.is_authenticated:
         return redirect(url_for('home'))
     form = LoginForm()
     if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('log In Unsuccessful Please Check Your Email and Password','danger')
     return render_template('login.html', title = 'login' , form = form) 

@app.route('/logout',)
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/account', methods = ['GET','POST'])
@login_required
def account():
     form=UpdateAccountForm()
     if form.validate_on_submit():
          current_user.firstName=form.firstName.data
          current_user.secondName=form.secondName.data
          current_user.date=form.date.data
          current_user.email=form.email.data
          current_user.today = date.today()
          db.session.commit()
          flash(f'Your Account has been updated !!', 'success')
          redirect(url_for('account'))
     elif request.method == 'GET':
          form.firstName.data=current_user.firstName
          form.firstName.data=current_user.secondName
          form.date.data=current_user.date
          form.email.data=current_user.email
     return render_template('account.html', title = 'Account',form = form)
@app.route('/send_reset_email')
def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender='rajpoutfazi@gmail.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return redirect(url_for('login'))
@app.route('/reset_password', methods = ['GET','POST'])
def reset_request():
     if current_user.is_authenticated: 
        return redirect(url_for('home'))
     form=RequestResetForm()
     if form.validate_on_submit():
         user=User.query.filter_by(email=form.email.data).first()
         send_reset_email(user)
         flash(f'Email has been send to you  with an instruction to reset password!!', 'info')
         return redirect(url_for('login'))
     return render_template('reset.html', title = 'Reset Password',form = form)
@app.route('/reset_password/<token>', methods = ['GET','POST'])
def reset_token(token):
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     user=User.verify_reset_token(token)
     if user is None:   
         flash(f'That is invalid or expired token !!', 'warning')
         return redirect(url_for('reset_request'))
     form=ResetPasswordForm()
     if form.validate_on_submit():
         hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user.password= hashed_password
         db.session.commit()
         flash(f'Your password has been updated!!','success') #showing success msg if user created account successfuly
         return redirect(url_for('login'))
     return render_template('reset_token.html', title = 'Reset Password',form = form)

  
