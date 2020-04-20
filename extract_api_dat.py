from pyzomato import Pyzomato
import json
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('PROJECT_API_KEY')

p = Pyzomato(API_KEY)

# Create an empty list, that will be used to append each dictionary returned.
restaurantList = []

# Create a loop that iterates five times starting from 0th record and increases by increments of 20
for a in range(0,100,20):
    restaurants = p.search(lat=51.509865,lon=-0.118092,
                           count=20,
                           sort='rating',
                           order='desc',
                           category=10,
                           start=a)
    print(a)
    restaurantList.append(restaurants)

# Write list of dictionaries to a json file
with open('Top60London.json', 'w') as fp:
    json.dump(restaurantList, fp)