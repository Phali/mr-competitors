import requests
import googlemaps
import json
import time
import csv

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
    
    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

class GoogleDM(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


#Generate an API key on your Google Cloud and save it on an external file 
#called creds.py
# (https://developers.google.com/places/web-service/intro)
        
from creds import api_key
api = GooglePlaces(api_key)

kavak_shw = {"Lerma": "19.278630, -99.484617", "Florencia": "19.424953, -99.166439", 
              "Fortuna": "19.483682, -99.133187" , "Santa_Fe": "19.377280, -99.254569", "Tlalplan": "19.283918, -99.176300"}

fields = ['name', 'formatted_address', 'website', 'rating']
place_dict = []
queries = ['auto_broker', 'vendetuauto', 'soloautos', 'car_dealer']
ya_vistos = {}

for query in queries:
    print(query)
    for place in kavak_shw:
        print(place)
        json_data = api.search_places_by_coordinate(kavak_shw[place], "5000", query)
        for x in json_data:
           if (x['place_id'] not in ya_vistos) and ('kavak' not in x['name'].lower()):
               ya_vistos[x['place_id']] = 1
               details = api.get_place_details(x['place_id'], fields)
               details['result']['lat'] = x['geometry']['location']['lat']
               details['result']['lng'] = x['geometry']['location']['lng']
               try:
                   place_dict.append(details['result'])
               except:
                   pass

csv_columns = fields
csv_columns.append('lat')
csv_columns.append('lng')

csv_file = "market_research_raw.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in place_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")
