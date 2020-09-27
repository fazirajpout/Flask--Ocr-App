from flask import Flask             
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
app = Flask(__name__)

app.config['SECRET_KEY']= '495e79ea53913e058769bea37a04fb48'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_view = 'login'
#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] ='rajpoutfazi@gmail.com'
#app.config['MAIL_PASSWORD'] = 'hjyhszzavpewvzfe'
#app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = 'rajpoutfazi@gmail.com'
#app.config['MAIL_PASSWORD'] = 'hjyhszzavpewvzfe'
#mail = Mail(app)

from ocrapp import routes 
