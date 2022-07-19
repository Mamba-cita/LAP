from http import client
from locale import currency
from unicodedata import category
from xml.dom.minidom import Document
from flask import Flask
from app import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required,UserMixin





class LapModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug=db.Column(db.String(200), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_job = db.Column(db.String(), nullable=True)
    profile_image = db.Column(db.String(200))
    user_roles = db.relationship('User_roles', backref='user_roles')
    transporter_id = db.relationship('Transporter', backref='transporter')
    client=db.relationship('Client', backref='clients')
    order=db.relationship('Orders', backref='order')
    posts = db.relationship('Posts', backref='posts')
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
     

class User_roles(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return '<User_roles %r>' % self.id
    



class Client(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Shipments = db.relationship('Shipments', backref='shipment')
    account_manager=db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class Transporter(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    account_manager=db.Column(db.String(80), nullable=False)
    account_manager=db.Column(db.String(80), nullable=False) 
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class Shipments(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    ron = db.Column(db.Integer)
    Shipments_type = db.Column(db.String(80), nullable=False)
    commodity = db.Column(db.String(80), nullable=False)
    total_allocation = db.Column(db.Integer, nullable=False)
    acc_manager = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Orders(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=False)
    transport_rate = db.Column(db.Integer, nullable=False)
    truck_reg =db.Column(db.String(80), nullable=False)
    qty_to_load = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now()) 
    created_by= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    