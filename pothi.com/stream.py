from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey='vs2JKRsczp8OSNWVe6BpXM7Sn'
csecret='TLEwzLdz1KCE9WRbgGDhYpRgU2dFFK4iFH9DCKAJZns36HqDti'

atoken='918711119664910336-bU2GyXU5zckxlkPeSQMYA3eMJUSxLwh'
asecret='KtEZavmuNDkom4dgJqdr51gorRuHjDykO9bMiIEuHNa1E'



class listener(StreamListener):
    

    def on_data(self,data):
        print data
        return True

    def on_error(self,status):
        print status


auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth,listener())
twitterStream.filter(track=["car"])
