from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os

consumer_token = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# authentication block - not final location!
auth = OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

words = ["women", "scholarship"]
word = ["scholarship"]
stuff = ["twitter"]
print(consumer_token, consumer_secret, access_token, access_token_secret)
# QUEUE =  []

class Listener:
    """custom listener from the tweepy class to change method"""

    @classmethod
    def creation(cls, constraints):
        filters = " ".join(constraints)
        myStreamListener = MyStreamListener
        myStream = Stream(auth, listener=myStreamListener())
        myStream.filter(track=[filters], async=True)


class MyStreamListener(StreamListener):

    def on_status(self, status):
        print(status.text)
        # QUEUE.append(status.text)




# if __name__ == '__main__':
#     # authentication block - not final location!
#     auth = OAuthHandler(consumer_token, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)

Listener.creation(words)
