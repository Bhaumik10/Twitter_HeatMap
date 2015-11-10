import json
import pymongo
import tweepy

consumer_key = "BTI88V737AGyfrvvifSY3dypB"
consumer_secret = "fEG6P0c5QuBcM0deiY3TICuL9j4DEjbI707TZATYDGMVl3QOiw"
access_key = "80275400-CSFtyGNbQm5WAqyWCFkPqeUbcHJSS5X9iC3QaEnIB"
access_secret = "Gzq2hjMJCWllxfVvXd04rhYhTrJYkahIrEsBaZHISVQ8w"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        #self.db = pymongo.MongoClient('127.0.0.1',27017).test # data goes on test db schema
        self.db = pymongo.MongoClient('127.0.0.1',27017).test # data goes on local db schema

    def on_data(self, tweet):  # tweet is the name of our collection in mongoDB.
        print(json.loads(tweet))
        self.db.tweets.insert(json.loads(tweet))

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['a'])