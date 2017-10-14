# To run this code, first edit config.py with your configuration, then:

# python twitter_stream_download.py -q your keyword
# Output will be displayed every minute in sorted order in a text file 'count.txt' and the prompt 

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import time
from datetime import datetime,timedelta
import process_time

import json_reader
import json_reader2
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import memcache
 
import operator
import collections
from operator import itemgetter
from collections import Counter
import os



count_all2 = Counter()
time_all={}
start_time = datetime.now()

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""


    def on_data(self, data):
        try:
            global start_time
            terms_cur = json_reader2.process_text(data) #The processed terms in current tweet
            time_cur = process_time.process_datetime(data) #DateTime object for current tweet
            term_time = {term:time_cur for term in terms_cur} #A ditionary for storing term times of current tweet
            time_all.update(term_time) #A dictionary for storing all terms
            
            count_all2.update(terms_cur) #A counter to update score of terms
            mc.set_multi(count_all2) #A cache is maintained and updated
            terms = list(count_all2) 
            
            for term in terms:
                #Reduce score when term does not appear for 30s
                if (datetime.utcnow()-time_all[term])>timedelta(seconds = 30): 
                    count_all2[term]= count_all2[term] -1
                #Delete terms when score falls below 0
                if count_all2[term]<0:
                    del count_all2[term]
                    mc.delete(term)
            
            #Printing every 60 seconds in sorted form according to score
            if (datetime.now() - start_time)> timedelta(seconds = 60):
                start_time = datetime.now()
                os.system('clear')
                with open('count.txt', 'w', encoding='utf-8') as f:
                    for k,l in sorted([(j,i) for i,j in count_all2.items()],reverse=True):
                        f.write(l+' : '+str(k)+'\n')
                        try:
                            print(l+' : '+str(k))
                        except:
                            continue
                        
            return True
        except BaseException as e:
            pass
        return True

    def on_error(self, status):
        pass

if __name__ == '__main__':

    #Accepting the keyword arguments
    parser = get_parser()
    args = parser.parse_args()
    
    #Configuring the connection
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    #Starting the Streaming API process
    while True:
        try:
            twitter_stream = Stream(auth, MyListener(args.query))
            twitter_stream.filter(track=[args.query])
        except:
            pass
        
