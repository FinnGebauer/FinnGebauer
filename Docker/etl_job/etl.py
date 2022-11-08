import pymongo
import re
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


time.sleep(10)

#create sentiment analysis object
s  = SentimentIntensityAnalyzer()

# Establish a connection to the MongoDB server
mongo = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = mongo.twitter

#create postgresdb
pg = create_engine('postgresql://postgres:postgres@postgresdb:5432/all_tweets', echo=True)

#Create tables
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP, 
    text VARCHAR(500),
    sentiment NUMERIC
);
''')

#RegEx that help cleaning the data
mentions_regex = '@[A-Za-z0-9]+'
url_regex = 'https?:\/\/\S+'

def regex_clean(text):
    text = re.sub(mentions_regex, '', text)
    text = re.sub(url_regex, '', text)
    return text

#EXTRACT
def extract():
    extracted_tweets = db.tweets.find()
    return extracted_tweets

#TRANSFORM AND SENTIMENT ANALYSIS
def transform(extracted_tweets):
    transformed_tweets = []
    for tweet in extracted_tweets:
        tweet['text'] = regex_clean(tweet['text'])
        sentiment = s.polarity_scores(tweet['text']) 
        tweet['sentiment'] = sentiment['compound']
        transformed_tweets.append(tweet)
    return transformed_tweets

#LOAD
def load(transformed_tweets):
    for tweet in transformed_tweets:
        try:
            query = "INSERT INTO tweets VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;"
            pg.execute(query, (tweet['id'], tweet['created_at'], tweet['text'], tweet['sentiment']))
        except:
            pass


entries = extract()
entries = transform(entries)
load(entries)