from db import db

class StoreModel(db.Model):
	__tablename__='stores'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))						#80 chars max for username
	#do back ref link; confirms the relationship in stores table
	items = db.relationship('ItemModel', lazy='dynamic')	#self.items is now a query builder; until call json below will not list all items; makes app faster
	
	def __init__(self, name):			#since all items have name; now the item is an object not a dict
		self.name = name
		
	def json(self):
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]}		#this is what is always returned to user; list of items in store
		
	@classmethod
	def find_by_name(cls, name):		#find store by name
		return StoreModel.query.filter_by(name=name).first()		#sqlalchemy query: Select * from items where name=name limit 1
	
	def save_to_db(self):										#for updating or inserting
		db.session.add(self)
		db.session.commit()
		
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()