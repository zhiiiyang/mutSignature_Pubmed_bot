import json
import tweepy
from datetime import date
from datetime import timedelta 
from pymed import PubMed
import os

def lambda_handler(event, context):
  retweet_pubmed_bot()
  return {
    'statusCode':200
  }

def retweet_pubmed_bot():
  auth = tweepy.OAuthHandler(os.environ['api_key'], os.environ['api_secret_key'])
  auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
  api = tweepy.API(auth)
  timeline = api.user_timeline("mutsignatures", count = 100)
  id_strs = []
  for status in timeline:
      if 'RT @' in status.text:
          id_strs.append(status.retweeted_status.id)
  yesterday = date.today()- timedelta(days = 1)
  search_terms = ['#MutationalSignatures','#MutationalSignature', 'mutational signatures', 'mutational signature']
  for i in range(len(search_terms)):
      for status in tweepy.Cursor(api.search, q = search_terms[i], lang = "en", since = yesterday).items(100):
          if status.id not in id_strs and status.author.name != "mutational signatures twitbot" and 'RT @' not in status.text:
              #print(status.id)
              api.retweet(status.id)
              
  #pubmed twitter            
  pubmed = PubMed(tool="MyApp", email="zhiyang@usc.edu")
  results = pubmed.query('\"mutational signature\" AND (("2020/01/01"[Date - Create] : "3000"[Date - Create]))', max_results=1000)
  # Loop over the retrieved articles
  keyword = "mutational signature"
  tweets_text = [i.text for i in timeline] 
  for article in results:
    if all(article.title[0:10] not in substring for substring in tweets_text):
        #print(article.title + " " + " https://doi.org/" + article.doi)
        #print(article.doi)
        api.update_status(article.title + " " + " https://doi.org/" + article.doi)
        break
