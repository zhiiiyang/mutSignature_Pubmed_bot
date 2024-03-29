import json
import tweepy
import datetime
from pymed import PubMed
import os

def lambda_handler(event, context):
  retweet_pubmed_bot()
  return {
    'statusCode':200
  }

def retweet_pubmed_bot():
  auth = tweepy.OAuth1UserHandler(
    os.environ['api_key'], os.environ['api_key_secret'],
    os.environ['access_token'], os.environ['access_token_key']
  )
  api = tweepy.API(auth)
  timeline = api.user_timeline(user_id="mutsignatures", count = 100)
  id_strs = []
  for status in timeline:
    if 'RT @' in status.text:
        id_strs.append(status.retweeted_status.id)
  search_terms = ['#MutationalSignatures','#MutationalSignature', 'mutational signatures', 'mutational signature']

  for search_term in search_terms:
    tweets=api.search_tweets(search_term, count=50, lang="en")
    for tweet in tweets:
      if tweet.id not in id_strs and tweet.author.name != "mutational signatures twitbot" and 'RT @' not in tweet.text:
        api.retweet(tweet.id)
              
  #pubmed twitter            
  pubmed = PubMed(tool="MyApp", email="zhiyang@usc.edu")
  results = pubmed.query('\"mutational signature\" AND (("2020/01/01"[Date - Create] : "3000"[Date - Create]))', max_results=3)
  # Loop over the retrieved articles
  keyword = "mutational signature"
  tweets_text = [i.text for i in timeline] 
  for article in results:
    if all(article.title not in substring for substring in tweets_text):
        #print(result.title + + "https://doi.org/" + result.doi)
        api.update_status((article.title[:(140-4-len("https://doi.org/" + article.doi))] + "... https://doi.org/" + article.doi))
        break
