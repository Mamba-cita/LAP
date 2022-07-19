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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://osrvqpiwtijbhg:e95ec46d831e0ad054a1b445f46a09657ca427d48101147dab2cf1cc20401126@ec2-3-217-14-181.compute-1.amazonaws.com:5432/d934grvl1taucq'
 

GOOGLE_CLIENT_ID =  "522885775133-vjh6nl0glerfvd7vpgbglmqv9qtqua3h.apps.googleusercontent.com"

ckeditor = CKEditor(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import views
from app import models



app.config.from_object('config')