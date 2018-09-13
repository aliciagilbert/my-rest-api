from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	#not going allow editing of stores, so no put resource
	def get(self, name):
		store = StoreModel.find_by_name(name)	#looks in db to see if its there
		if store:					#if store exists
			return store.json()		#if there return it
		else:
			return {'message': 'Store not found'}, 404
			
	
	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': "A store with name '{}' already exists.".format(name)}, 400
		
		store = StoreModel(name)		#if didn't exist create it
		try:
			store.save_to_db()			#try to save it to db
		except:
			return {'message': 'An error occured while creating the store.'}, 500	#something wrong with server
		
		return store.json(), 201		#201=store has been created	
		
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		return {'message': 'Store deleted.'}
		
		
class StoreList(Resource):
	def get(self):
		return {'stores': [store.json() for store in StoreModel.query.all()]}