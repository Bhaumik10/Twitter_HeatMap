#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "80275400-CSFtyGNbQm5WAqyWCFkPqeUbcHJSS5X9iC3QaEnIB"
access_token_secret = "Gzq2hjMJCWllxfVvXd04rhYhTrJYkahIrEsBaZHISVQ8w"
consumer_key = "BTI88V737AGyfrvvifSY3dypB"
consumer_secret = "fEG6P0c5QuBcM0deiY3TICuL9j4DEjbI707TZATYDGMVl3QOiw"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data

        with open('/users/Bhaumik/twitter_data/tweets.txt','a') as tf:
            tf.write(data)
        return True
        #print(lenght(data))
        #file = open('/users/Bhaumik/twitter_data/tweets.txt','a+',1)
        

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript' ,'ruby'])