#saving all posted items; no longer need sqlite3 after sqlalchemy; no longer making connections to db like that
#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#every resource/endpoint must be a class
class Item(Resource):
	#define this for use throughout the class
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float,
		required=True,
		help="This filed cannot be left blank!"
	)							#will only modify price data of request; all else ignored
	parser.add_argument('store_id', 
		type=int,
		required=True,
		help="Every item needs a store id!"
	)
	
	#used to have classmethods here, but is a model not a resource so put in models		
		
	@jwt_required()									#need to authenticate before we can get
	def get(self, name):	
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()						#recall json is a model
		return {'message': 'Item not found'}, 404
		
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400	#400 means something went wrong with request; user error
					
		data = Item.parser.parse_args()
		item = ItemModel(name, data['price'], data['store_id'])		
		try:
			item.save_to_db()
		except:
			return {"message": "An error occured inserting item."}, 500		#if there is an error inserting; 500 is internal server error not user error
		return item.json(), 201					#201 is status code for created; return this to user
		
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()		
		return {'message': 'Item deleted'}		
		
	def put(self, name):
		data = Item.parser.parse_args()			#put valid args from json payload in data variable

		item = ItemModel.find_by_name(name)
		
		if item is None:						#item did not exist so insert
			item = ItemModel(name, data['price'], data['store_id'])		#we can unpack here as **data
		else:
			item.price = data['price']
		item.save_to_db()
		
		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}		#ItemModel.query.all() returns all the objects in the db
		