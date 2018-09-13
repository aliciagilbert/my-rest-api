from werkzeug.security import safe_str_cmp		#to compare strings; used here to compare pwds
from models.user import UserModel

#authenticate the user function this time using data.db
def authenticate(username, password):
	user = UserModel.find_by_username(username)			#set default value = None
	if user and safe_str_cmp(user.password, password):	#implied user is not None; compares pw in table with pw send by user
		return user

def identity(payload):
	user_id = payload['identity']
	return UserModel.find_by_id(user_id)
