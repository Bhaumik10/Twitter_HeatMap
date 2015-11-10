
# contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
# <html>
# <head>
# <script src="http://maps.googleapis.com/maps/api/js?key=AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0"></script>

# <script>

# var loc=new google.maps.LatLng(52.3667,4.9000);
# function initialize()
# {
# var mapProp = {
#   center:loc,
#   zoom:5,
#   mapTypeId:google.maps.MapTypeId.ROADMAP
#   };
  
# var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

# var myCity = new google.maps.Circle({
#   center:loc,
#   radius:20000,
#   strokeColor:"#ff0000",
#   strokeOpacity:1,
#   strokeWeight:3,
#   fillColor:"##ff0000",
#   fillOpacity:0.3
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
gmaps = googlemaps.Client(key='AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0')
client = MongoClient(server,port)

db = client.test

collection = db.test.tweets
tweets_data = []
tweets_file = db.tweets.find({"user.friends_count": {'$gt' : 100} ,'$and' : [{"place.bounding_box.type" : "Polygon"},{"place.full_name": {'$ne' :"null" }}]},{"place.bounding_box.coordinates" :1,"text":1,"user.friends_count":1,"place.full_name":1,"user.time_zone":1,"user.location":1,"entities.hashtags":1,"retweet_count":1,"user.verified":1,"user.followers_count":1,"user.followers_count":1,"user.geo_enabled":1,"user.name":1,"user.lang":1,"user.screen_name":1,"user.created_at":1,"place.country":1,"place.place_type":1,"place.country_code":1,"created_at":1}).limit(1)

for tweet in tweets_file:
  try:
    tweets_data.append(tweet)
    
  except:
    continue

hashTags = []

print "Total Number of Tweets we are currently Analyzing....",len(tweets_data)

tweets = pd.DataFrame(tweets_data)
for j in range(0,len(tweets_data)):
  print "User's Longitude #1 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]
  print "User's Latitude #1 :: ",tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]

  lat = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]
  longi = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]
  cord_pair = str(lat)+","+str(longi)
  print(cord_pair)
  contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
  <html>
  <head>
  <script src="http://maps.googleapis.com/maps/api/js?key=AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0"></script>

  <script>

  var loc=new google.maps.LatLng('''+cord_pair+''');
  function initialize()
  {
  var mapProp = {
    center:loc,
    zoom:5,
    mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    
  var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
  
  var myCity = new google.maps.Circle({
    center:loc,
    radius:2000,
    strokeColor:"#ff0000",
    strokeOpacity:1,
    strokeWeight:3,
    fillColor:"##ff0000",
    fillOpacity:0.3
    });

  myCity.setMap(map);
  }

  google.maps.event.addDomListener(window, 'load', initialize);
  </script>
  </head>

  <body>
  <div id="googleMap" style="height:100%;width:100%;margin:0 auto;"></div>
  </body>

  </html>
  '''


  


def main():
    browseLocal(contents)

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='tempBrowseLocal.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac

main()


# for x in range(0,len(coordinate_ar)):
#   point = coordinate_ar[x]
#   print point



