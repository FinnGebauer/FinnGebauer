import tweepy
import os
import pymongo

##################
# Authentication #
##################
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)


mongo = pymongo.MongoClient(host="mongodb", port=27017)
db = mongo.twitter

########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

#response = client.get_user(
#    username='en_cohen',
    #user_fields=['created_at', 'description', 'location',
    #             'public_metrics', 'profile_image_url']
#)

#user = response.data

#print(dict(user))


#########################
# Get a user's timeline #
#########################

# https://docs.tweepy.org/en/stable/pagination.html#tweepy.Paginator
# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

#cursor = tweepy.Paginator(
#    method=client.get_users_tweets,
#    id=user.id,
#    exclude=['replies', 'retweets']#,
#   #tweet_fields=['author_id'], 'created_at', 'public_metrics']
#).flatten(limit = 50)

#for tweet in cursor:
#    db.tweets.insert_one(dict(tweet))


#####################
# Search for Tweets #
#####################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

# - means NOT
search_query = "Ian Cohen -is:retweet -is:reply -is:quote lang:en -has:links"

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    tweet_fields=['id', 'created_at']
).flatten(limit=500)

for tweet in cursor:
    print(tweet.text+'\n')
