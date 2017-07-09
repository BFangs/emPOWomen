import tweepy
import os

consumer_token = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# authentication block - not final location!
authorization = tweepy.OAuthHandler(consumer_token, consumer_secret)
authorization.set_access_token(access_token, access_token_secret)

words = ["women", "scholarship"]
results = tweepy.api.search("scholarship")
print(results)
# api.search(q="scholarship", lang ='en', since_id=1, show_user=True)
