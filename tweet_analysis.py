from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import googlemaps
from googlemaps import client as _client
import test as _test
#import gmaps

#Database(MongoClient('localhost', 27017), u'test')

server="127.0.0.1"
port = 27017
gmaps = googlemaps.Client(key='AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0')
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

print "Total Number of Tweets we are currently Analyzing....",len(tweets_data)

tweets = pd.DataFrame(tweets_data)
for j in range(0,len(tweets_data)):
	print "This is whole data frame :: ",tweets_data[j]
	print "This is object id :: ",tweets_data[j]['_id']
	print "Tweet Text :: ",tweets_data[j]['text'].encode("utf-8")
	print "Tweet Time :: ",tweets_data[j]['created_at']
	print "Retweet Count :: ",tweets_data[j]['retweet_count']
	print "User's HashTags :: ",tweets_data[j]['entities']['hashtags']
	try:
		hashTags = tweets_data[j]['entities']['hashtags']
		for k in range(0,len(hashTags)):
			print "HashTag :: ",hashTags[k]['text'].encode("utf-8")
	except (IndexError):
			print
	print "Tweet Language :: ",tweets_data[j]['user']['lang']

	print "User's Name :: ",tweets_data[j]['user']['name'].encode("utf-8")
	print "Verified user or Not? :: ",tweets_data[j]['user']['verified']
	print "Account Creation Date :: ",tweets_data[j]['user']['created_at']
	print "User Time Zone :: ",tweets_data[j]['user']['time_zone']
	print "User Screen name :: ",tweets_data[j]['user']['screen_name']
	print "User's Friend Count :: ",tweets_data[j]['user']['friends_count']
	print "User's Follower Count :: ",tweets_data[j]['user']['followers_count']
	#print "User's Statuses Count :: ",tweets_data[j]['user']['statuses_count']
	print "User's reTweet Count :: ",tweets_data[j]['retweet_count']
	print "User's Geo Enabled? :: ",tweets_data[j]['user']['geo_enabled']
	try:
		print "User's location :: ",tweets_data[j]['user']['location'].encode("utf-8")
	except (AttributeError, TypeError):
		print 
	print "User's country name :: ",tweets_data[j]['place']['country'].encode("utf-8")
	print "User's Place type :: ",tweets_data[j]['place']['place_type']
	print "User's Longitude #1 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]
	print "User's Latitude #1 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]
	print "User's longitude & Latitude #1 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][0]
	print "User's longitude & Latitude #2 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][1]
	print "User's longitude & Latitude #3 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][2]
	print "User's longitude & Latitude #4 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][3]
	print "User's country code :: ",tweets_data[j]['place']['country_code'].encode("utf-8")
	#geolocator = Nominatim()
	lati = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]
	#print(lati)
	longi=tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]

	cord_pair = "\""+str(lati)+" , "+str(longi)+"\""
	print cord_pair
	
	reverse_geocode_result = gmaps.reverse_geocode((lati,longi))
	detail = pd.DataFrame(reverse_geocode_result)
	print "Address of the user based on Latitude & Longitude :: ",detail['formatted_address'][0]
# 	contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
# <html>
# <head>
# <script src="http://maps.googleapis.com/maps/api/js?key=AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0"></script>
# <script>
	
# var loc=new google.maps.LatLng(latitude,longitude);
# function initialize()
# {
# var mapProp = {
#   center:loc,
#   zoom:3,
#   mapTypeId:google.maps.MapTypeId.TERRAIN
#   };
  
# var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

# var myCity = new google.maps.Circle({
#   center:loc,
#   radius:20000,
#   strokeColor:"#ff0000",
#   strokeOpacity:0.8,
#   strokeWeight:2,
#   fillColor:"##ff0000",
#   fillOpacity:0.1
#   });

# myCity.setMap(map);
# }

# google.maps.event.addDomListener(window, 'load', initialize);

# </script>
# </head>

# <body>
# <div id="googleMap" style="height:100%;width:100%;margin:0 auto;"></div>
# </body>

# </html>
# '''
# def main():
#     browseLocal(contents)

# def strToFile(text, filename):
#     """Write a file with the given name and the given text."""
#     output = open(filename,"w")
#     output.write(text)
#     output.close()

# def browseLocal(webpageText, filename='tempBrowseLocal.html'):
#     '''Start your webbrowser on a local file containing the text
#     with given filename.'''
#     import webbrowser, os.path
#     strToFile(webpageText, filename)
#     webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac

# main()
print "*********************************************"


