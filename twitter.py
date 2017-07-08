import twitter
import tweepy
import re
import os

consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY'],
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# authentication block - not final location!
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class listen(tweepy.StreamListener):
    """custom listener from the tweepy class to change method"""

    def on_status(self, status):
        print(status.text)


if __name__ == __'main'__:
