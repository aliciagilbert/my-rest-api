import sqlite3

connection = sqlite3.connect('data.db')					#create connection to file data.db 

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)" 	#define schema
cursor.execute(create_table)			#execute

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

#to insert many users
users = [
	(2, 'rolf', 'asdf'),
	(3, 'anne', 'xyz')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
	print row

connection.commit()						#to save changes to db

connection.close()