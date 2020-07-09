#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from urllib3.exceptions import ProtocolError,ReadTimeoutError

import json

#Variables that contains the user credentials to access Twitter API
access_token = "911609571885633541-4EwvGuoHKFDlXSS22WC21wWOq8qqFse"
access_token_secret = "aHsqcWUCce7rcrwh9e6vKQOwUJf2x30FXzQYbM81uMCmI"
consumer_key = "DZBKOKfoWsshSYUe1NI3ba91I"
consumer_secret = "WL3mlr7GudRbIkXRSB762MDrplwYPnAvdwXB5pwAgiYTeERNTR"

politics = ["Modi" ,"Narendra Modi ", "PMO India ", "Arvind Kejriwal ", "Arun Jaitley ", "Amit Shah ", "Sushma Swaraj ", "Rajnath Singh ", "BJP ","Bhartiya Janata Party","Bhartiya Janta Party ", "Akhilesh Yadav ", "Smriti Z Irani ", "Rahul Gandhi ", "Subramanian Swamy ", "Shashi Tharoor ", "Manohar Parrikar ", "ShivrajSingh Chouhan ", "Piyush Goyal ", "AAP ","Aam Aadmi Party", "Indian National Congress ", "Lalu Prasad Yadav ", "Nitin Gadkari ", "N Chandrababu Naidu ", "Vasundhara Raje ", "Devendra Fadnavis ", "Yogi Adityanath ", "Omar Abdullah ", "Ravi Shankar Prasad ", "HMO India ", "CM Office, GoUP ", "Nandan Nilekani ", "Vijay Rupani ", "Dr Raman Singh ", "Kapil Sibal ", "Nirmala Sitharaman ", "Raveesh Kumar ", "Kalam Center ", "Aaditya Thackeray ", "Sushil Kumar Modi ", "Manish Sisodia ", "Dr. Harsh Vardhan ", "Milind Deora ", "Samajwadi Party ", "Shahnawaz Hussain ", "Vijay Kumar Singh ", "Prakash Javadekar ", "Tejashwi Yadav "]
choices1 = ['bjp', 'aap', 'bhajpaa', 'bhartiya janata party', 'aam aadmi party',
           'bahujan samaj party', 'Samajwadi Party', 'AIADMK', 'DMK', 'Trinamool Congress', 'Shiv Sena',
           'Nationalist Congress Party', 'Biju Janata Dal', 'Janata Dal United', 'JDU', 'Rastriya Janata Dal', 'RJD',
           'JDS', 'Communist Party of India', 'Communist Party of India- Marxist', 'CPI-M', 'CPI']

politics.extend(choices1)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        f.write(data)
        tweet=json.loads(data)
        #print(tweet['text'])

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    f=open('/Users/anubhavjain/Desktop/twitter_data_1.txt','a+')
    #This line filter Twitter Streams to capture data by the given keywords:
    #stream.filter(follow=["207809313"])
    while (True):
        try:
            stream.filter(track=politics, locations=[68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078], languages=['en', 'hi', 'tl', 'bn', 'bh', 'gu', 'kn', 'ks', 'ml', 'mr', 'pa', 'sa', 'ta', 'te'], filter_level='low')
        except (ProtocolError,AttributeError,ReadTimeoutError,ConnectionError):
            continue;
