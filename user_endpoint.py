from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):


	# GET method to return data stored in users.csv
	def get(self):
		data = pd.read_csv('users.csv') # Read csv with pandas
		data = data.to_dict() # Convert dataframe to dictionary
		return {'data': data}, 200 # Return data and 200 OK code
	
	# POST method to append data to users.csv	
	def post(self):
		parser = reqparse.RequestParser() # initialize
		
		# Add arguments
		parser.add_argument('userId', required = True)
		parser.add_argument('name', required = True)
		parser.add_argument('city', required = True)
		
		args = parser.parse_args() # Parse arguments into dictionary
		
		
		
		# Read and Append changes to datframe
		data = pd.read_csv('users.csv') # Read
		
		# Check to see if new data conflicts with existing data
		if args['userId'] in list(data['userId']):
			return{
				'message': f"'{args['userId']}' already exists."
			}, 69420
		
		else:
			# Create new dataframe containing new values
			new_data = pd.DataFrame({
				'userId': args['userId'],
				'name': args['name'],
				'city': args['city'],
				'locations':[[]]
			})
		
		data = data.append(new_data, ignore_index = True) # Append
		data.to_csv('users.csv', index = False) # Save new
		return{'data': data.to_dict()}, 200 # Return data with 200 OK
		
	
class Locations(Resource):

	# methods go here
	pass
	
api.add_resource(Users, '/users') # '/users' is the entry point for Users
api.add_resource(Locations, '/locations') # '/locations' is entry point for Locations

if __name__ == '__main__':
	app.run() # run Flask app
	
