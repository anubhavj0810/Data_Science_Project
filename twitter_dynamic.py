# Code for extracting the data on basis of given keywords and modelling it

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from wordcloud import WordCloud
from urllib3.exceptions import ProtocolError,ReadTimeoutError

import re
import json
import pandas as pd
import matplotlib
import numpy as np
import datetime as dt
import multiprocessing
from multiprocessing import Process
import sys
#import time

print("Default encoding is .. ",sys.getdefaultencoding())
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Variables that contains the user credentials to access Twitter API
access_token = "911609571885633541-4EwvGuoHKFDlXSS22WC21wWOq8qqFse"
access_token_secret = "aHsqcWUCce7rcrwh9e6vKQOwUJf2x30FXzQYbM81uMCmI"
consumer_key = "DZBKOKfoWsshSYUe1NI3ba91I"
consumer_secret = "WL3mlr7GudRbIkXRSB762MDrplwYPnAvdwXB5pwAgiYTeERNTR"


count_temp=0
fig,ax = plt.subplots()
fig1,ax1 = plt.subplots()
fig2,ax2 = plt.subplots()
fig3,ax3 = plt.subplots()
fig4,ax4 = plt.subplots()

fig.set_size_inches(20, 15)
fig1.set_size_inches(20, 15)
fig2.set_size_inches(20, 15)
fig3.set_size_inches(20, 15)
fig4.set_size_inches(20, 15)

politics = ["Modi" ,"Narendra Modi ", "PMO India ", "Arvind Kejriwal ", "Arun Jaitley ", "Amit Shah ", "Sushma Swaraj ", "Rajnath Singh ", "BJP ","Bhartiya Janata Party","Bhartiya Janta Party ", "Akhilesh Yadav ", "Smriti Z Irani ", "Rahul Gandhi ", "Subramanian Swamy ", "Shashi Tharoor ", "Manohar Parrikar ", "ShivrajSingh Chouhan ", "Piyush Goyal ", "AAP ","Aam Aadmi Party", "Indian National Congress ", "Lalu Prasad Yadav ", "Nitin Gadkari ", "N Chandrababu Naidu ", "Vasundhara Raje ", "Devendra Fadnavis ", "Yogi Adityanath ", "Omar Abdullah ", "Ravi Shankar Prasad ", "HMO India ", "CM Office, GoUP ", "Nandan Nilekani ", "Vijay Rupani ", "Dr Raman Singh ", "Kapil Sibal ", "Nirmala Sitharaman ", "Raveesh Kumar ", "Kalam Center ", "Aaditya Thackeray ", "Sushil Kumar Modi ", "Manish Sisodia ", "Dr. Harsh Vardhan ", "Milind Deora ", "Samajwadi Party ", "Shahnawaz Hussain ", "Vijay Kumar Singh ", "Prakash Javadekar ", "Tejashwi Yadav ","Dravida Munnetra Kazhagam "]
politics1 = ['bjp', 'aap', 'bhajpaa', 'bhartiya janata party', 'aam aadmi party',
           'bahujan samaj party', 'Samajwadi Party', 'AIADMK', 'DMK', 'Trinamool Congress', 'Shiv Sena',
           'Nationalist Congress Party', 'Biju Janata Dal', 'Janata Dal United', 'JDU', 'Rastriya Janata Dal', 'RJD',
           'JDS', 'Communist Party of India', 'Communist Party of India- Marxist', 'CPI-M', 'CPI']


choices = ['CONGRESS', 'BJP', 'AAP','#AAP','@AAP', 'BHAJPAA', 'BHARTIYA JANATA PARTY', 'AAM AADMI PARTY', 'BAHUJAN SAMAJ PARTY', 'BSP', 'SAMAJWADI PARTY', 'SP','@SP','#SP','AIADMK', 'DMK', 'TRINAMOOL CONGRESS', 'SHIV SENA', 'NATIONALIST CONGRESS PARTY', 'BIJU JANATA DAL', 'JANATA DAL UNITED', 'JDU', 'RASTRIYA JANATA DAL', 'RJD','#RJD','@RJD', 'JDS','#JDS','@JDS','COMMUNIST PARTY OF INDIA', 'COMMUNIST PARTY OF INDIA- MARXIST', 'CPI-M', 'CPI','#CPI','@CPI']
choices_party = ['INC', 'BJP', 'AAP', 'AAP', 'AAP', 'BJP', 'BJP', 'AAP', 'BSP', 'BSP', 'SP', 'SP', 'SP', 'SP', 'AIADMK', 'DMK',
                 'Trinamool Congress', 'Shiv Sena', 'Nationalist Congress Party', 'Biju Janata Dal',
                 'Janata Dal United', 'Janata Dal United', 'Rastriya Janata Dal', 'Rastriya Janata Dal', 'Rastriya Janata Dal', 'Rastriya Janata Dal', 'JDS', 'JDS', 'JDS',
                 'CPI', 'CPI-M', 'CPI-M', 'CPI', 'CPI', 'CPI']
choices_party1 = dict(zip(choices_party, [0 for i in range(len(choices_party))]))
choices_party_live = dict(zip(choices_party, [0 for i in range(len(choices_party))]))

pattern1 = "(?i)congress|bjp| aap |#aap|@aap|bhajpaa|bhartiya janata party|aam aadmi party|bahujan samaj party|BSP|Samajwadi Party| SP |@SP|#SP|AIADMK|DMK|Trinamool Congress|Shiv Sena|Nationalist Congress Party|Biju Janata Dal|Janata Dal United|JDU|Rastriya Janata Dal| RJD |#RJD|@RJD|JDS|#JDS|@JDS|Communist Party of India|Communist Party of India- Marxist|CPI-M| CPI |#CPI|@CPI"
politics.extend(politics1)


def locations(t):
    if(t['user']['location'] != None):
        if(t['user']['location'].split(',')[0].strip().upper() != 'INDIA'):
            return t['user']['location'].split(',')[0].strip().upper()
    else:
        return None

def Geo_Party(query):
    party = re.findall(pattern1,query)
    ind = []
    for i in party:
        ind.append(choices_party[choices.index(i.strip().upper())])

    ind = np.unique(np.array(ind))
    return ind

def Hashtags_tweets(time_int):
    #count_var = 0
    a = tweets_twi['time']
    time_min = []
    time_min_time = []

    x_temp=1
    while(x_temp <= len(a)):
        if(not a[len(a) - x_temp] != a[len(a) - x_temp]):
            start_time = a[len(a) - x_temp].split()
            del(start_time[4])
            start_time[4] = start_time[4][2:]
            start_time = " ".join(start_time)
            time_min.append(tweets_twi['text'][len(a) - x_temp])
            start_dt = dt.datetime.strptime(start_time, '%a %b %d %H:%M:%S %y')
            time_min_time.append(start_dt)
            break;
        else:
            time_min.append(tweets_twi['text'][len(a) - x_temp])
            time_min_time.append(tweets_twi['time'][len(a) - x_temp])
            x_temp=x_temp + 1

    for i in range(len(a)-x_temp-1,-1,-1):
        #count_var = count_var + 1
        #print(count_var," p1")
        if(not a[i]!=a[i]):
            a[i]=a[i].split()
            if(len(a[i])==6):
                del(a[i][4])
                a[i][4] = a[i][4][2:]
            a[i] = " ".join(a[i])

            a_dt = dt.datetime.strptime(a[i],'%a %b %d %H:%M:%S %y')

            diff = start_dt - a_dt
            diff = diff.seconds
            if(diff/60 > time_int):
                break;
            else:
                time_min.append(tweets_twi['text'][i])
                start_dt = max(start_dt, a_dt)
                time_min_time.append(a_dt)
        else:
            time_min.append(tweets_twi['text'][i])
            time_min_time.append(tweets_twi['time'][i])

    queue_local.put([time_min,time_min_time])
    return time_min,time_min_time

def Hastag_extract(tweets_array):
    hashtag=[]

    for i in tweets_array:
        try:
            ht = re.findall("#[\w]*", i.encode('ascii','ignore').decode('ascii'))
            hashtag.extend(ht)
        except Exception:
            pass

    return hashtag

def Word_cloud(all_words):
    all_words = " ".join(all_words)
    word_cloud = WordCloud(width=800,height=500,random_state=21,max_font_size=110).generate(all_words)
    plt.imshow(word_cloud,interpolation='bilinear')
    plt.axis('off')

def Stats_live(time_int):
    global start_tweet_time,end_tweet_time

    #count_var = 0
    a = tweets_twi['time']
    tweets_twi_live = pd.DataFrame(columns=['time','username','text','lang','country','user_loc'])
    x_temp=1
    while(x_temp <= len(a)):
        if(not a[len(a) - x_temp] != a[len(a) - x_temp]):
            start_time = a[len(a) - x_temp].split()
            del(start_time[4])
            start_time[4] = start_time[4][2:]
            start_time = " ".join(start_time)
            tweets_twi_live = tweets_twi.loc[len(a) - x_temp:len(a) - x_temp]
            start_dt = dt.datetime.strptime(start_time, '%a %b %d %H:%M:%S %y')
            break;
        else:
            tweets_twi_live = tweets_twi.loc[len(a) - x_temp:len(a) - x_temp]
            x_temp=x_temp+1

    for i in range(len(a)-x_temp-1,-1,-1):
        #count_var = count_var + 1
        #print(count_var," p2 ")

        if(not a[i]!=a[i]):
            a[i]=a[i].split()
            if(len(a[i])==6):
                del(a[i][4])
                a[i][4] = a[i][4][2:]
            a[i] = " ".join(a[i])

            a_dt = dt.datetime.strptime(a[i],'%a %b %d %H:%M:%S %y')

            diff = start_dt - a_dt
            diff = diff.seconds
            if(diff/60 > time_int):
                break;
            else:
                tweets_twi_live = tweets_twi_live.append(tweets_twi.loc[i:i],ignore_index=True)
                start_dt = max(start_dt, a_dt)
                end_tweet_time = a_dt
                start_tweet_time = start_dt
        else:
            tweets_twi_live = tweets_twi_live.append(tweets_twi.loc[i:i],ignore_index=True)
    queue_local.put(tweets_twi_live)
    queue_global.put([start_tweet_time,end_tweet_time])
    return tweets_twi_live


def Append_data(tweets_twitter,tweet_data):
    if (tweet_data['place'] != None):
        tweets_twitter = tweets_twitter.append({'country': tweet_data['place']['country'].upper(),'time': tweet_data['created_at'],'text': tweet_data['text'],'lang': tweet_data['lang'],'username': tweet_data['user']['name'],'user_loc': locations(tweet_data)}, ignore_index=True)
    else:
        tweets_twitter = tweets_twitter.append({'country': None,'time': tweet_data['created_at'],'text': tweet_data['text'],'lang': tweet_data['lang'],'username': tweet_data['user']['name'],'user_loc': locations(tweet_data)}, ignore_index=True)

    return tweets_twitter

def Append_data_begin(tweets_twitter,tweet_data):
    s = pd.DataFrame()
    if (tweet_data['place'] != None):
        s = s.append({'country': tweet_data['place']['country'].upper(),'time': tweet_data['created_at'],'text': tweet_data['text'],'lang': tweet_data['lang'],'username': tweet_data['user']['name'],'user_loc': locations(tweet_data)}, ignore_index=True)
    else:
        s = s.append({'country': None,'time': tweet_data['created_at'],'text': tweet_data['text'],'lang': tweet_data['lang'],'username': tweet_data['user']['name'],'user_loc': locations(tweet_data)}, ignore_index=True)

    tweets_twitter = pd.concat([s,tweets_twitter],ignore_index=True,sort=False)
    return tweets_twitter

def Modelling_data(tweets_twitter,ax,ax1,ax2,ax3,title1,title2,title3,title4):
    tweets_by_lang = tweets_twitter['lang'].value_counts()

    if (len(tweets_by_lang) >= 3):
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('Languages', fontsize=15)
        ax.set_ylabel('Number of tweets', fontsize=15)
        ax.set_title(title1, fontsize=15, fontweight='bold')
        tweets_by_lang[:3].plot(ax=ax, kind='bar', color='green')

        f = open('/Users/anubhavjain/Desktop/Contents_twitter.txt', 'w+')
        f.write("Tweet Count till now .. \n")
        f.write(str(tweet_count))
        f.write("\n\n"+ title1 +"\n")
        f.writelines(str(tweets_by_lang[:3]).encode('ascii','ignore').decode('ascii'))
        f.close()

    tweets_by_country = tweets_twitter['country'].value_counts()

    if (len(tweets_by_country) >= 5):
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlabel('Countries', fontsize=15)
        ax1.set_ylabel('Number of tweets', fontsize=15)
        ax1.set_title(title2, fontsize=15, fontweight='bold')
        tweets_by_country[:5].plot(ax=ax1, kind='bar', color='blue')

        f = open('/Users/anubhavjain/Desktop/Contents_twitter.txt', 'a+')
        f.write("\n\n"+ title2 +"\n")
        f.writelines(str(tweets_by_country[:5]).encode('ascii','ignore').decode('ascii'))
        f.close()

    tweets_by_loc = tweets_twitter['user_loc'].value_counts()

    if (len(tweets_by_loc) >= 5):
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.set_xlabel('Locations', fontsize=15)
        ax2.set_ylabel('Number of tweets', fontsize=15)
        ax2.set_title(title3, fontsize=15, fontweight='bold')
        tweets_by_loc[:5].plot(ax=ax2, kind='bar', color='blue')

        f = open('/Users/anubhavjain/Desktop/Contents_twitter.txt', 'a+')
        f.write("\n\n"+ title3 +"\n")
        f.writelines(str(tweets_by_loc[:5]).encode('ascii','ignore').decode('ascii'))
        f.close()

    tweets_by_username = tweets_twitter['username'].value_counts()

    if (len(tweets_by_username) >= 5):
        ax3.tick_params(axis='x', labelsize=15)
        ax3.tick_params(axis='y', labelsize=10)
        ax3.set_xlabel('UserName', fontsize=15)
        ax3.set_ylabel('Number of tweets', fontsize=15)
        ax3.set_title(title4, fontsize=15, fontweight='bold')
        tweets_by_username[:5].plot(ax=ax3, kind='bar', color='blue')

        f = open('/Users/anubhavjain/Desktop/Contents_twitter.txt', 'a+')
        f.write("\n\n"+ title4 +"\n")
        f.writelines(str(tweets_by_username[:5]).encode('ascii','ignore').decode('ascii'))
        f.close()

class StdOutListener(StreamListener):

    def on_data(self, data):
        global tweet_count
        global tweets_twi
        global count_temp
        global hash_10,time_10,tweets_twi_10
        global ax,ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9
        global start_tweet_time,end_tweet_time
        global decision
        global X

        file.write(data)
        tweet = json.loads(data)
        tweet_count = tweet_count + 1

        if(count_temp == 0):
            print("The following are the features of the data/tweets")
            for key in tweet.keys():
                print(key)

            print("\n")

        Append_data(tweets_twi,tweet)

        key_arr = Geo_Party(tweet['text'])
        for i in key_arr:
            choices_party1[i] += 1

        Modelling_data(tweets_twi,ax,ax1,ax2,ax3,'Top 3 Languages','Top 5 Countries','Top 5 locations','Top 5 TwitterUsers')
        Word_cloud(Hastag_extract(tweets_twi['text']))
        if(count_temp % 10 == 0):
            plt.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Popular_Hastags.jpg')
            # plt.close()
            # plt.figure()
        party = dict(sorted(choices_party1.items(), key=lambda x: x[1], reverse=True)[:5])
        ax4.tick_params(axis='x', labelsize=15)
        ax4.tick_params(axis='y', labelsize=10)
        ax4.set_xlabel('Parties', fontsize=15)
        ax4.set_ylabel('Count', fontsize=15)
        ax4.set_title('Top 5 Parties', fontsize=15, fontweight='bold')
        ax4.bar(party.keys(), party.values(), align='center', color='yellow')

        ### Many tweets are being retweeted and thus appearing many a times in the dataframe.
        # tweets_by_text = tweets_twi['text'].value_counts()
        # print(tweets_by_text)


        if(decision == 'Y'):

            if(not tweet['created_at'] != tweet['created_at']):
                tweet_time = tweet['created_at'].split()
                del(tweet_time[4])
                tweet_time[4] = tweet_time[4][2:]
                start_time = " ".join(tweet_time)
                tweet_time = dt.datetime.strptime(start_time, '%a %b %d %H:%M:%S %y')

                difference_time = start_tweet_time - end_tweet_time
                difference_time = difference_time.seconds

                if (tweet_time == start_tweet_time or difference_time/60 < X):
                    start_tweet_time = max(tweet_time,start_tweet_time)
                    hash_10.insert(0, tweet['text'])
                    time_10.insert(0, tweet_time)
                    Append_data_begin(tweets_twi_10,tweet)
                    key_arr = Geo_Party(tweet['text'])
                    for i in key_arr:
                        choices_party_live[i] += 1
                else:
                    start_tweet_time = max(tweet_time,start_tweet_time)
                    hash_10.insert(0, tweet['text'])
                    time_10.insert(0, tweet_time)
                    Append_data_begin(tweets_twi_10, tweet)

                    key_arr = Geo_Party(tweet['text'])
                    for i in key_arr:
                        choices_party_live[i] += 1


                    while(True):
                        if(time_10[len(time_10) - 1] != time_10[len(time_10) - 1]):
                            time_10.pop()
                            tweets_twi_10 = tweets_twi_10.loc[:len(tweets_twi_10)-2,:]
                            key_del = Geo_Party(hash_10.pop())
                            for j in key_del:
                                choices_party_live[j] -= 1

                        elif((start_tweet_time - time_10[len(time_10) - 1]).seconds / 60 > X):
                            time_10.pop()
                            tweets_twi_10 = tweets_twi_10.loc[:len(tweets_twi_10)-2,:]
                            key_del = Geo_Party(hash_10.pop())
                            for j in key_del:
                                choices_party_live[j] -= 1

                        else:
                            end_tweet_time = time_10[len(time_10) - 1]
                            break;
            else:
                hash_10.insert(0, tweet['text'])
                time_10.insert(0, tweet['created_at'])
                Append_data_begin(tweets_twi_10, tweet)
                key_arr = Geo_Party(tweet['text'])
                for i in key_arr:
                    choices_party_live[i] += 1
            #print(start_tweet_time, end_tweet_time, start_tweet_time - end_tweet_time)


        if(count_temp % (10*X) == 0):
            print("\nTweet Count till now .. \t")
            print(tweet_count, "\n\n")
            print(start_tweet_time, end_tweet_time, start_tweet_time - end_tweet_time)

        if(decision == 'Y'):
            """tweets_twi_10 = Stats_live(X)
            Modelling_data(tweets_twi_10, ax5, ax6, ax7, ax8, 'Top 3 Languages recently', 'Top 5 Countries recently','Top 5 locations recently', 'Top 5 TwitterUsers recently')
            hash_10,time_10 = Hashtags_tweets(X)
            for i in hash_10:
                key_arr = Geo_Party(str(i))
                for j in key_arr:
                    choices_party1[j] += 1
            print(start_tweet_time,end_tweet_time,start_tweet_time-end_tweet_time)"""

            Modelling_data(tweets_twi_10, ax5, ax6, ax7, ax8, 'Top 3 Languages recently','Top 5 Countries recently', 'Top 5 locations recently', 'Top 5 TwitterUsers recently')
            Word_cloud(Hastag_extract(hash_10))
            # print(tweets_twi_10)

            party1 = dict(sorted(choices_party_live.items(), key=lambda x: x[1], reverse=True)[:5])
            ax9.tick_params(axis='x', labelsize=15)
            ax9.tick_params(axis='y', labelsize=10)
            ax9.set_xlabel('Parties', fontsize=15)
            ax9.set_ylabel('Count', fontsize=15)
            ax9.set_title('Top 5 Parties in last '+ str(X) +' mins ', fontsize=15, fontweight='bold')
            ax9.bar(party1.keys(), party1.values(), align='center', color='yellow')

        #plt.pause(0.00001)

        #time.sleep(0.0001)

        if(count_temp % 10 == 0):
            fig.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Language.jpg')
            fig1.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Country.jpg')
            fig2.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Locations.jpg')
            fig3.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Users.jpg')
            fig4.savefig('/Users/anubhavjain/Desktop/Flask2/static/Overall_Parties.jpg')
            fig5.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Languages.jpg')
            fig6.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Country.jpg')
            fig7.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Locations.jpg')
            fig8.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Users.jpg')
            fig9.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Parties.jpg')
            plt.savefig('/Users/anubhavjain/Desktop/Flask2/static/Recent_Popular_Hastags.jpg')


        count_temp = count_temp + 1
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API

    tweets_twi = pd.DataFrame()
    tweet_count = 0
    tweets_data=[]
    start_tweet_time = -1
    end_tweet_time = -1


    f_temp = open('/Users/anubhavjain/Desktop/twitter_data_1.txt', 'r')

    for line in f_temp:
        try:
            tweet1 = json.loads(line)
            tweets_data.append(tweet1)

        except(Exception):
            continue

    f_temp.close()

    tweets_data = np.array(tweets_data)
    tweet_count=len(tweets_data)

    ### to write any Random tweet from the dataset
    if(len(tweets_data)>0):
        f = open('/Users/anubhavjain/Desktop/Random_tweet_streaming.txt', 'w+')
        f.write("Printing random tweet along with its features ....\n\n")
        for i in tweets_data[np.random.randint(len(tweets_data),size=None)].items():
            str_temp = str(i) + "\n\n"
            str_temp = str_temp.encode('ascii','ignore').decode('ascii')
            f.write(str_temp)
        f.close()


    tweets_twi['time'] = list(map(lambda t: t['created_at'], tweets_data))
    tweets_twi['text'] = list(map(lambda t: t['text'], tweets_data))
    tweets_twi['lang'] = list(map(lambda t: t['lang'], tweets_data))
    tweets_twi['country'] = list(map(lambda t: t['place']['country'].upper() if (t['place'] != None) else None,tweets_data))

    list_temp = []
    for i in tweets_data:
        list_temp.append(locations(i))
    tweets_twi['user_loc'] = list_temp

    tweets_twi['username'] = list(map(lambda t: t['user']['name'], tweets_data))


    tweets_twi['user_loc'] = tweets_twi['user_loc'].replace('USA','UNITED STATES')
    tweets_twi['user_loc'] = tweets_twi['user_loc'].replace('BOMBAY','MUMBAI')
    tweets_twi['user_loc'] = tweets_twi['user_loc'].replace('BANGALORE','BENGALURU')
    tweets_twi['user_loc'] = tweets_twi['user_loc'].replace('DELHI', 'NEW DELHI')

    for i in tweets_data:
        key_arr = Geo_Party(i['text'])
        for j in key_arr:
            choices_party1[j] += 1

    queue_local = multiprocessing.Queue()
    queue_global = multiprocessing.Queue()

    print("Do you want to see the Statistics for last X minutes Y/N ...")
    decision = input()
    decision = decision.upper()

    if(decision == 'Y'):
        print("Enter the value of X")
        X = int(input())
        p1 = Process(target=Hashtags_tweets,args=(X,))
        p2 = Process(target=Stats_live,args=(X,))
        p1.start()
        p2.start()

        #p1.join()
        #p2.join()
        hash_10,time_10 = queue_local.get()
        tweets_twi_10 = queue_local.get()
        start_tweet_time,end_tweet_time = queue_global.get()


        print("No. of tweets in last " +str(X)+ " mins",len(tweets_twi_10))
        for i in np.array(tweets_twi_10['text']):
            key_arr = Geo_Party(str(i))
            for j in key_arr:
                choices_party_live[j] += 1

        fig5, ax5 = plt.subplots()
        fig6, ax6 = plt.subplots()
        fig7, ax7 = plt.subplots()
        fig8, ax8 = plt.subplots()
        fig9, ax9 = plt.subplots()
        plt.figure(figsize=(10, 7))

        fig5.set_size_inches(20, 15)
        fig6.set_size_inches(20, 15)
        fig7.set_size_inches(20, 15)
        fig8.set_size_inches(20, 15)
        fig9.set_size_inches(20, 15)



    file = open('/Users/anubhavjain/Desktop/twitter_data_1.txt', 'a+')
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)


    # This line filter Twitter Streams to capture data by the given keywords and on basis of the given location as india and languages as hindi and english:
    #stream.filter(follow=["207809313"])

    while (True):
        try:
            stream.filter(track=politics, locations=[68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078], languages=['en', 'hi', 'tl', 'bn', 'bh', 'gu', 'kn', 'ks', 'ml', 'mr', 'pa', 'sa', 'ta', 'te'], filter_level='low')
        except (ProtocolError, AttributeError,ReadTimeoutError):
            continue;