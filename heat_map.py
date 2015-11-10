from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
import googlemaps
from googlemaps import client as _client
import test as _test
import cgi
import cgitb

cgitb.enable()
server="127.0.0.1"
port = 27017
gmaps = googlemaps.Client(key='AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0')
client = MongoClient(server,port)

db = client.test

collection = db.test.tweets
tweets_data = []
tweets_file = db.tweets.find({"user.friends_count": {'$gt' : 1} ,'$and' : [{"place.bounding_box.type" : "Polygon"},{"place.full_name": {'$ne' :"null" }},{"text" : {'$regex': u"music"}}]},{"place.bounding_box.coordinates" :1,"text":1,"user.friends_count":1,"place.full_name":1,"user.time_zone":1,"user.location":1,"entities.hashtags":1,"retweet_count":1,"user.verified":1,"user.followers_count":1,"user.followers_count":1,"user.geo_enabled":1,"user.name":1,"user.lang":1,"user.screen_name":1,"user.created_at":1,"place.country":1,"place.place_type":1,"place.country_code":1,"created_at":1})

for tweet in tweets_file:
  try:
    tweets_data.append(tweet)
    
  except:
    continue

hashTags = []
data = []
coordinate_ar = []

print "Total Number of Tweets we are currently Analyzing....",len(tweets_data)

tweets = pd.DataFrame(tweets_data)
for j in range(0,len(tweets_data)):
  lat = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][1]
  longi = tweets_data[j]['place']['bounding_box']['coordinates'][0][0][0]
  latlang = (lat,longi)
  latlang1 = [lat,longi]
  cord_pair = 'new google.maps.LatLng'+str(latlang)+','

  coordinate_ar.insert(j,cord_pair)

for i in range(0,len(coordinate_ar)): 
    data.append(coordinate_ar[i])

def print_st():
    l = "\n".join(data) 
    return l


contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta charset="utf-8">
    <title>Heatmaps</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
#floating-panel {
  position: absolute;
  top: 10px;
  left: 25%;
  z-index: 5;
  background-color: #fff;
  padding: 5px;
  border: 1px solid #999;
  text-align: center;
  font-family: 'Roboto','sans-serif';
  line-height: 30px;
  padding-left: 10px;
}

      #floating-panel {
        background-color: #fff;
        border: 1px solid #999;
        left: 25%;
        padding: 5px;
        position: absolute;
        top: 10px;
        z-index: 5;
      }

#search_box {
  position: absolute;
  top: 10px;
  right: 5%;
  z-index: 5;
  background-color: #fff;
  padding: 5px;
  border: 1px solid #999;
  text-align: center;
  font-family: 'Roboto','sans-serif';
  line-height: 30px;
  padding-left: 10px;
}
    </style>
  </head>

  <body>
    <div id="floating-panel">
      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
      <button onclick="changeGradient()">Change gradient</button>
      <button onclick="changeRadius()">Change radius</button>
      <button onclick="changeOpacity()">Change opacity</button>
    </div>
    <form id="frm1" action="/Users/Bhaumik/Documents/heat_map.py" method="get">
    <div id="search_box">
      <input id="pac-input" name="Trend_box" class="controls" type="text" placeholder="Enter Trending Word"/>
      <button onclick="search_trend()"> Search Trend </button>
    </div>
    </form>
    <div id="map"></div>
    <script>

var map;


function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 2,
    center: {lat: 52.3667, lng: 4.9000},
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: getPoints(),
    map: map
  });
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function search_trend() {
  var trend_word = document.getElementById('pac-input').value
  document.getElementById("search_box").innerHTML =
"Looking for " + trend_word + " Trend ";
    return trend_word;


}


function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

// Heatmap data: 500 Points
function getPoints() {

  return [ 
  

'''+str(print_st())+'''
      
  ];
}

    

</script>
<script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCAsYu2nBfJMo_pDNr8ZW6ki3oUh7cHCD0&signed_in=true&libraries=visualization&callback=initMap">
</script>
<p id="demo"></p>
</body>
</html>
'''

def main():
    browseLocal(contents)
    print '''search_trend();'''

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w") 
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='Tweet_heatMap.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac

main()




