#create item models = representation an item does and looks like
#not called by api method itself but is just used by code
#sql alchemy makes querying easier
from db import db

class ItemModel(db.Model):
	__tablename__='items'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))						#80 chars max for username
	price = db.Column(db.Float(precision=2))
	#add this column to link items to stores table by id
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))	#store in storemodel defined as int; links item and store table
	store = db.relationship('StoreModel')
	
	def __init__(self, name, price, store_id):			#since all items have name and price; now the item is an object not a dict
		self.name = name								#these lines assigns the input values to this model
		self.price = price
		self.store_id = store_id
		
	def json(self):
		return {'name': self.name, 'price': self.price}		#this is what is always returned to user
		
	@classmethod
	def find_by_name(cls, name):
		return ItemModel.query.filter_by(name=name).first()		#sqlalchemy query: Select * from items where name=name limit 1
	
	def save_to_db(self):										#for updating or inserting
		db.session.add(self)
		db.session.commit()
		
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()