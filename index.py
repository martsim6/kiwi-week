import requests
import argparse

# sending url request
def send_req(url):
	request = requests.get(url)
	# if request pass fine, return it, if not, print error
	if request.status_code == 200:
		return request
	else:
		print('Request failed with finish code {}'.format(request.status_code))


# function for searching needed data from API json
def get_needed_data(whole_data):
	items = []
	for data in whole_data:
		# searching airports in UK, so here we're finding United Kingdom, should be anything else
		if data['city']['country']['name'] == "United Kingdom":
			row = {
				"City Name" : data['city']['name'],
				"Airport Name" : data['name'],
				"IATA Code" : data['code'],
				"Latitude" : data['location']['lat'],
				"Longitude" : data['location']['lon']
			}
			# create and return list with dictionaries
			items.append(row)
	return items

# function for creating casual arguments for running program
def create_opt_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--cities", help='get cities with airports', action='store_true')
	parser.add_argument("--coords", help='get coordinates of each airport', action='store_true')
	parser.add_argument("--iata", help='get IATA codes', action='store_true')
	parser.add_argument("--names", help='get name of each airport', action='store_true')
	parser.add_argument("--full", help='get all details from each airport', action='store_true')
	args = parser.parse_args()
	return args
	
# function for decision which argument print what kind of values
def print_arg_value(data, args):
	for item in data:
		if args.cities:
			print("City name: {}".format(item['City Name']))
		elif args.coords:
			print("Coordinates - Latitude: {} Longitude: {}".format(item['Latitude'], item['Longitude']))
		elif args.iata:
			print("IATA code: {}".format(item['IATA Code']))
		elif args.names:
			print("Airport name: {}".format(item['Airport Name']))
		elif args.full:
			print("City name: {}, Airport name: {}, IATA code: {}, Coordinates - Lat: {}, Lon {}".format(item['City Name'], item['Airport Name'], item['IATA Code'], item['Latitude'], item['Longitude']))
		else:
			print('Airport Name: {}, Airport IATA Code: {}.'.format(item['Airport Name'], item['IATA Code']))

if __name__ == '__main__':

	args = create_opt_arguments()
	url = 'https://api.skypicker.com/locations?type=subentity&term=GB&locale=en-US&active_only=true&location_types=airport&limit=10000&sort=name'
	get_data = send_req(url)
	data_to_check = get_data.json()['locations']
	data_needed = get_needed_data(data_to_check)
	print_arg_value(data_needed, args)