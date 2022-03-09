
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
		
		data = pd.read_csv('users.csv') # Read dataframe
		
		# Check if new data conflicts with existing data
		if args['userId'] in list(data['userId']):
			return{
				'message': f"'{args['userId']}' already exists."
			}, 404
		
		else:
			# Create new dataframe containing new values
			new_data = pd.DataFrame({
				'userId': args['userId'],
				'name': args['name'],
				'city': args['city'],
				'locations':[[]]
			})
		
		# Append and save new users.csv
		data = data.append(new_data, ignore_index = True) # Append
		data.to_csv('users.csv', index = False) # Save new
				
		return{'data': data.to_dict()}, 200 # Return data with 200 OK
		
	# PUT method appends data to existing user. Similar to POST method	
	def put(self):
		parser = reqparse.RequestParser() # Initialize 
		
		# Add arguments
		parser.add_argument('userId', required = True)
		parser.add_argument('location', required = True) 
		
		args = parser.parse_args() # Parse arguments into dictionary
		
		# Read csv
		data = pd.read_csv('users.csv')
		
		# Check if user exists in data
		if args['userId'] in list(data['userId']):
			
			# Evaluate strings of lists to lists
			data['locations'] = data['locations'].apply(
				lambda x: ast.literal_eval(x)
			)
			
			# Select user
			user_data = data[data['userId'] == args['userId']]
			
			# Update user location
			user_data['locations'] = user_data['locations'].values[0] \
				.append(args['location'])		
				
			# Save updated location to users.csv
			data.to_csv('users.csv', index = False)
			
			# Return data and 200 OK
			return{'data': data.to_dict()}, 200
			
		else:
			# Otherwise userId does not exist
			return{
				'message': f"'{args['userId']}' user not found."
				}, 404
	
	# DELETE method removes userId from users.csv			
	def delete(self):
		parser = reqparse.RequestParser() # initialize
		
		# Add arguments
		parser.add_argument('userId', required = True)
		
		args = parser.parse_args() # Parse arguments to dictionary
		
		# Read csv
		data = pd.read_csv('users.csv')
		
		# Check is user exists
		if args['userId'] in list(data['userId']):
			
			# Remove user from users.csv
			data = data[data['userId'] != args['userId']]
			
			# Save updated users.csv
			data.to_csv('users.csv', index=False)
			
			# Return data and 200 OK
			return {'data':  data.to_dict()}, 200
		else:
			# Return 404 if user does not exists
			return {
				'message': f"'{args['userId']}' user not found."
			}, 404
			
	
class Locations(Resource):

	# GET method to return data stored in locations.csv
	def get(self):
		data = pd.read_csv('locations.csv') # Read csv with pandas
		#data = data.to_dict() # Convert dataframe to dictionary
		return {'data': data.to_dict()}, 200 # Return data and 200 OK code
		
		
	# POST method to append data to locations.csv	
	def post(self):
		parser = reqparse.RequestParser() # initialize
		# Add arguments
		parser.add_argument('locationId', required = True, type=int) # Specify int value
		parser.add_argument('name', required = True)
		parser.add_argument('rating', required = True, type=float) # Specify float value
		
		args = parser.parse_args() # Parse arguments into dictionary
		
		data = pd.read_csv('locations.csv') # Read dataframe
		
		# Check if new data conflicts with existing data
		if args['locationId'] in list(data['locationId']):
			return{
				'message': f"'{args['locationId']}' already exists."
			}, 404
		
		else:
			# Create new dataframe containing new values
			new_data = pd.DataFrame({
				'locationId': [args['locationId']],
				'name': [args['name']],
				'rating': [args['rating']],
			})
		
		# Append and save new users.csv
		data = data.append(new_data, ignore_index = True) # Append
		data.to_csv('locations.csv', index = False) # Save new				
		return{'data': data.to_dict()}, 200 # Return data with 200 OK
		
	# PUT method appends data to existing user. Similar to POST method	
	def patch(self):
		parser = reqparse.RequestParser() # Initialize parser
		
		# Add arguments
		parser.add_argument('locationId', required = True, type=int)
		parser.add_argument('name', store_missing = False) # Optional 
		parser.add_argument('rating', store_missing = False, type=int) # Optional 
		args = parser.parse_args() # Parse arguments into dictionary
		
		# Read csv
		data = pd.read_csv('locations.csv')
		
		# Check if location exists in data
		if args['locationId'] in list(data['locationId']):
						
			# Select locationId 
			user_data = data[data['locationId'] == args['locationId']]
			
			# Update name if locationId exists
			if 'name' in args:
				user_data['name'] = args['name']		

			# Update rating if locationId exists
			if 'rating' in args:
				user_data['rating'] = args['rating']
				
			# Update user data
			data[data['locationId'] == args['locationId']] = user_data					
				
			# Save update to locations.csv
			data.to_csv('locations.csv', index = False)
			
			# Return data and 200 OK
			return{'data': data.to_dict()}, 200
			
		else:
			# Otherwise userId does not exist
			return{
				'message': f"'{args['locationId']}' location not found."
				}, 404
		
	# DELETE method removes locationId from locations.csv			
	def delete(self):
		
		parser = reqparse.RequestParser() # initialize
		parser.add_argument('locationId', required = True, type=int) # Add arguments, locationId
		args = parser.parse_args() # Parse arguments to dictionary
		
		# Read csv
		data = pd.read_csv('locations.csv')
		
		# Check is locationId exists
		if args['locationId'] in list(data['locationId']):
			# Remove lcoationId from locations.csv if it exists 
			data = data[data['locationId'] != args['locationId']]
			# Save updated locations.csv
			data.to_csv('locations.csv', index=False)
			# Return data and 200 OK
			return {'data':  data.to_dict()}, 200
		else:
			# Return 404 if lcoation does not exists
			return {
				'message': f"'{args['locationId']}' location not found."
			}, 404
	
	
class Obesity(Resource):

	# GET method returns data from obesity.csv
	def get(self):
		data = pd.read_csv('obesity.csv') # Read csv with pandas
		#data = data.to_dict() # Convert dataframe to dictionary
		return {'data': data.to_dict()}, 200 # Return data and 200 OK code

	def put(self):
		pass
	def post(self):
		pass
	def delete(self):
		pass
		
api.add_resource(Users, '/users') # '/users' is the entry point for Users
api.add_resource(Locations, '/locations') # '/locations' is entry point for Locations
api.add_resource(Obesity, '/obesity') # '/obesity' is the entry point for Obesity

if __name__ == '__main__':
	app.run() # run Flask app
	
