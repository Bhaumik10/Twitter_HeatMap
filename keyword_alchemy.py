from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import googlemaps
from googlemaps import client as _client
import test as _test

server="127.0.0.1"
port = 27017
#gmaps = googlemaps.Client(key='AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0')
client = MongoClient(server,port)
#print(c.test_database)
db = client.test
#print(db)
collection = db.test.tweets
#print(collection)

#print(db.collection_names(include_system_collections=False))

tweets_data = []
tweets_file = db.tweets.find({"user.friends_count": {'$gt' : 100} ,'$and' : [{"place.bounding_box.type" : "Polygon"},{"place.full_name": {'$ne' :"null" }}]},{"place.bounding_box.coordinates" :1,"text":1,"user.friends_count":1,"place.full_name":1,"user.time_zone":1,"user.location":1,"entities.hashtags":1,"retweet_count":1,"user.verified":1,"user.followers_count":1,"user.followers_count":1,"user.geo_enabled":1,"user.name":1,"user.lang":1,"user.screen_name":1,"user.created_at":1,"place.country":1,"place.place_type":1,"place.country_code":1,"created_at":1}).limit(10)
#first parameter is the query, second one is the projection.
for tweet in tweets_file:
	try:
		tweets_data.append(tweet)
		#print(tweet)
	except:
		continue

hashTags = []

print("Total Number of Tweets we are currently Analyzing....",len(tweets_data))

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

tweets = pd.DataFrame(tweets_data)
for j in range(0,len(tweets_data)):
	#print "This is whole data frame :: ",tweets_data[j]
	#print "This is object id :: ",tweets_data[j]['_id']
	print("processing Text :: ",tweets_data[j]['text'].encode("utf-8"))

	response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])



	