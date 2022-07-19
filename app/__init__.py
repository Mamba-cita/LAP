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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://grdqpgztaofikd:c189a3f66cde4f96a89bc0716542141452630431e84be32d1aa68d6047081aaf@ec2-3-219-229-143.compute-1.amazonaws.com:5432/dadt90sglqe560'
 

GOOGLE_CLIENT_ID =  "522885775133-vjh6nl0glerfvd7vpgbglmqv9qtqua3h.apps.googleusercontent.com"

ckeditor = CKEditor(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import views
from app import models



app.config.from_object('config')