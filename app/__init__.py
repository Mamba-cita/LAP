from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_ckeditor import CKEditor





app = Flask(__name__)

#key
app.config['SECRET_KEY'] = 'gigi'
#database
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/lap"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://aifitqjkjukjpp:fc2214723f2c4ae7ba1f0df7af84852bf6e355ecfbcf9d5734668c0786c15e32@ec2-52-204-157-26.compute-1.amazonaws.com:5432/de4nmfmn41davh"
 

GOOGLE_CLIENT_ID =  "522885775133-vjh6nl0glerfvd7vpgbglmqv9qtqua3h.apps.googleusercontent.com"

ckeditor = CKEditor(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import views
from app import models



app.config.from_object('config')