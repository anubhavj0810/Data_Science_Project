from flask import Flask, render_template, request, send_from_directory
import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor
import sys
import twitter
from TwitterSearch import *

CONSUMER_KEY = 'st7d9QVrd0m7xQIBR6gdJ2r0P'
CONSUMER_SECRET = 'TU5YGxiW1PoWf4quinHk6dK2GXOHnvhRvWVYKUiCZ9rF7lyVZh'
ACCESS_KEY = '911609571885633541-Hm7GziRUBgewSegS0MwtifSeliq0DAv'
ACCESS_SECRET = 'BWDt64ZB7IttIcoEjC5NI91GDaq0VZd9TwFKffZjaMaIk'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api1=twitter.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token_key=ACCESS_KEY,access_token_secret=ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

app = Flask(__name__)
#img_folder = os.listdir('static/')
#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

global c
global array
global choice_g

array = []
c = -1

def Reply(full_tweet,c1):
    replies = dict()	
    if(c1>2): ### Fixing the depth of the graph
        return replies	
    if (c1 == 0):
        value = 1000
    else:
        value = 100
        full_tweet = full_tweet._json	
    since = full_tweet['id']
    try:
        name = '@' + full_tweet['retweeted_status']['user']['screen_name']
        since = full_tweet['retweeted_status']['id']
    except Exception:
        name = '@' + full_tweet['user']['screen_name']	
    #if (c1 == 0):
    #print(name,c1)	
    replies[since] = []
    c1 += 1
    for tweet in Cursor(api.search ,q='to:' + name ,since_id = since , result_type ='recent' , timeout = 999999).items(value):
        #print(tweet.text)
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if(tweet.in_reply_to_status_id_str == str(since)):
                replies[since].append(Reply(tweet,c1))
                #replies.append(tweet.text)
    c1-=1
    return replies,since

def Tweets(a):
    global c
    c+=1
    for i in a:
    	if(type(i) is dict):
    		break;
    	x = i[0]
    	m = [j for j in x.keys()][0]
    	array.append(str(10*c*" ") + api1.GetStatus(status_id=m).AsDict()["user"]["screen_name"] + ": " + str(api1.GetStatus(status_id=m).AsDict()["text"]))
    	Tweets(x[m])
    c-=1


@app.route("/")
def mainpage():
    return render_template("mainpage.html")


@app.route("/index", methods=["GET","POST"])
def index():
	global choice_g
	headline = "Data Analysis Graphs"
	try:
		choice = request.form.get("name")
		choice = choice.upper()
		choice_g = choice
	except Exception as e:
		try:
			choice = choice_g
		except Exception as e:
			choice = "YES"
	print(choice)
	image_names1 = os.listdir('./static')

	if(choice == "YES"):
		image_names = []
		for i in image_names1:
				if(i[0]=="R"):
					image_names.append(i)
		return render_template("index.html", image_names=image_names, headline=headline)
	else:
		image_names = []
		for i in image_names1:
			if(i[0]=="O"):
				image_names.append(i)
		return render_template("index.html", image_names=image_names, headline=headline)

@app.route('/static/<path:filename>')
def send_image(filename):
    return send_from_directory('static', filename)

@app.route("/reply",methods=["POST"])
def reply():
	global array

	name = request.form.get("name")
	#count_max = request.form.get("count")
	if(name[0]!="@"):
		name = "@" + name
	reply_arr = []
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)	

	ts = TwitterSearch(consumer_key = CONSUMER_KEY,consumer_secret = CONSUMER_SECRET,access_token = ACCESS_KEY,access_token_secret = ACCESS_SECRET)
	tuo = TwitterUserOrder(name) # create a TwitterUserOrder
	count = 0	

	for full_tweets in ts.search_tweets_iterable(tuo):
	    count +=1
	    c1 = 0
	    tweet = full_tweets['text'].translate(non_bmp_map)
	    reply_arr,id_tweet = Reply(full_tweets,c1)
	    n_repl = len(reply_arr[id_tweet])
	    array_tweet = []
	    for elements in reply_arr[id_tweet]:
	    	Tweets([elements])
	    	array_tweet.append(array)
	    	array = []
	    return render_template("reply.html", headline=name[1:], array_tweet=array_tweet, n_repl=n_repl, tweet=tweet)


@app.route("/political")
def hello():
    #name = name.capitalize()
    return 20*1*"-"

if __name__ == '__main__':
	app.run(debug=True)
