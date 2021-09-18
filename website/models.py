from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	date_created = db.Column(db.DateTime(timezone=True), default = func.now())
	todos = db.relationship('Todos', backref = 'user', passive_deletes = True)

class Todos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	todo = db.Column(db.Text, nullable = False)
	date_created = db.Column(db.DateTime(timezone=True), default = func.now())
	author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable=False)