# retrieve user objects from db created from test.py instead of in memory db
#allow users to sign up
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
		
class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be blank."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be blank."
	)	
	
	def post(self):
		data = UserRegister.parser.parse_args()
		
		#check dup users
		if UserModel.find_by_username(data['username']):
			return {"message": "A user with that username already exists"}, 400
			
		user = UserModel(**data)	#because of user model use instead of data['username'], data['password']
		user.save_to_db()
		
		return {"message": "User created successfully."}, 201