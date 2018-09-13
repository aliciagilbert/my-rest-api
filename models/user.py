# retrieve user objects from db created from test.py instead of in memory db
#allow users to sign up
import sqlite3
from db import db

class UserModel(db.Model):									#class extends db model
	__tablename__='users'
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))						#80 chars max for username
	password = db.Column(db.String(80))
	
	def __init__(self, username, password):			#id is a python keyword so use _id
		self.username = username
		self.password = password
		
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	
	@classmethod											#add this to make code nicer and use the cls mentioned below
	def find_by_username(cls, username):					#change self to cls
		return cls.query.filter_by(username=username).first()		#1st username is in table
	
	@classmethod											#add this to make code nicer and use the cls mentioned below
	def find_by_id(cls, _id):								#change self to cls
		return cls.query.filter_by(id=_id).first()
		
