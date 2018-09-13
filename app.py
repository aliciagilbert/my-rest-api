#install Flask, Flask-JWT, Flaks-RESTful, Flask-SQLAlchemy
#note: name input is in url while parser data in json payload
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity			#in security.py
from resources.user import UserRegister				#need this to allow sign up; in resources/user.py
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'		#data.db found in root folder; could be mysql too
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	#turn off change tracking to save resources
app.secret_key = 'jose'
api = Api(app)

#use this to get rid of the create_tables file; no longer need to do that step
#after deploying to heroku put this in run.py file
'''
@app.before_first_request
def create_tables():
	db.create_all()									#before the first request runs create all tables
'''

jwt = JWT(app, authenticate, identity)				#creates endpoint /auth


api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/watch	; no need for app routes
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>') 
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':						#only run by explicitly running app.py; if run another file that imports this file, app.py will not run
	from db import db							#to prevent circular imports since importing in other models and resources
	db.init_app(app)
	app.run(port=5000, debug=True)				#gives more info to figure out what's wrong
