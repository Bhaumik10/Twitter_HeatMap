from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import googlemaps
from googlemaps import client as _client
import test as _test
import simplejson as json


server="127.0.0.1"
port = 27017
gmaps = googlemaps.Client(key='AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0')
client = MongoClient(server,port)

db = client.test

collection = db.test.tweets
tweets_data = []
tweets_file = db.tweets.find({'$and' : [{"place.bounding_box.type" : "Polygon"},{"place.full_name": {'$ne' :"null" }},{"text" : {'$regex': u"game"}}]},{"place.bounding_box.coordinates" :1,"text":1,"user.friends_count":1,"place.full_name":1,"user.time_zone":1,"user.location":1,"entities.hashtags":1,"retweet_count":1,"user.verified":1,"user.followers_count":1,"user.followers_count":1,"user.geo_enabled":1,"user.name":1,"user.lang":1,"user.screen_name":1,"user.created_at":1,"place.country":1,"place.place_type":1,"place.country_code":1,"created_at":1})

for tweet in tweets_file:
  try:
    tweets_data.append(tweet)
    
  except:
    continue

hashTags = []
coordinate_ar = []

print "Total Number of Tweets we are currently Analyzing....",len(tweets_data)

tweets = pd.DataFrame(tweets_data)
for j in range(0,len(tweets_data)):
  lat = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]
  longi = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]
  cord_pair = [lat,longi]
  #print(cord_pair)
  coordinate_ar.insert(j,cord_pair)
print(coordinate_ar)
#print(type(coordinate_ar))
contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="/Users/Bhaumik/Downloads/multiple_markers/css/style.css">
    <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?key=AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0"></script>
    <script type="text/javascript">
     var map;
     var infoWindow;

// markersData variable stores the information necessary to each marker

var markersData = '''+str(coordinate_ar)+'''

function initialize() {
   var mapOptions = {
      center: new google.maps.LatLng(52.3667,4.9000),
      zoom: 7,
      mapTypeId: 'roadmap',
   };

   map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

   // a new Info Window is created
   infoWindow = new google.maps.InfoWindow();

   // Event that closes the Info Window with a click on the map
   google.maps.event.addListener(map, 'click', function() {
      infoWindow.close();
   });

   // Finally displayMarkers() function is called to begin the markers creation
   displayMarkers();
}
google.maps.event.addDomListener(window, 'load', initialize);


// This function will iterate over markersData array
// creating markers with createMarker function
function displayMarkers(){

   // this variable sets the map bounds according to markers position
   var bounds = new google.maps.LatLngBounds();
   
   // for loop traverses markersData array calling createMarker function for each marker 
   for (var i = 0; i < markersData.length; i++){

      var latlng = new google.maps.LatLng(markersData[i][0], markersData[i][1]);
      

      createMarker(latlng);

      // marker position is added to bounds variable
      bounds.extend(latlng);  
   }

   // Finally the bounds variable is used to set the map bounds
   // with fitBounds() function
   map.fitBounds(bounds);
}

// This function creates each marker and it sets their Info Window content
function createMarker(latlng, name, address1, address2, postalCode){
   var marker = new google.maps.Marker({
      map: map,
      position: latlng,
      title: name
   });

   
}</script>
  </head>
  <body>
  <div>
    <input id="pac-input" class="controls" type="text" placeholder="Please Enter Key Word"/>
    <button>Click It !!</button>
  </div>
  
  <div id="map-canvas"></div>
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




