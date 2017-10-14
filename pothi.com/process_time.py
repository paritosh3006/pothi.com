from datetime import datetime
import json

def process_datetime(data):
        try:
            tweet = json.loads(data)
            
            tweet_time = datetime.strptime(tweet['created_at'][:10]+tweet['created_at'][30:],'%a %b %d %X %Y')
            
            return tweet_time
        except Exception as e:
            ii=1
       

