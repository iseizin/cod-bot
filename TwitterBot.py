#!/user/bin/env python
# -*- coding: utf-8 -*-


#########  参考文献 ###########
#タイムラインの検索：https://qiita.com/anyamaru/items/fda42dea27a510169b42#_reference-5edef372337422e4e3f7
#https://qiita.com/konojunya/items/59a68d35e44db8b87186
#形態素解析：https://www.jiriki.co.jp/blog/python/python-twitter-bot
###############################


C_KEY = "Your Consumer Key"
C_SECRET = "Your Consumer Secret"
A_KEY = "Your Access Token"
A_SECRET = "Your Access Token Secret"

from requests_oauthlib import OAuth1Session
from numpy.random import *
import json
import sys
import MeCab
import random
import re




timeline_url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
#url = "https://api.twitter.com/1.1/search/tweets.json?"   ←キーワード検索用？

params = {
     "lang": "ja",
    "result_type": "recent",
    "count": "20"  
    }
tw = OAuth1Session(C_KEY,C_SECRET,A_KEY,A_SECRET)
req = tw.get(timeline_url, params = params)

tweets = json.loads(req.text) 


def DataCollect():
    
    f = open("tweet.txt" , "w",encoding="utf-8")
    for i, tweet in enumerate(tweets): 
        f = open("tweet.txt" , "a",encoding="utf-8")
        print(tweet)
        list = tweet['text'].split()
        j=0
        for word in list:
            if word.find('http') != -1 or word.find("@") != -1 or word.find('RT') != -1: 
                del list[j] 
            j += 1

        f.writelines(list)
        f.close()




def SentenceGenerate():
    
    f = open("tweet.txt","r",encoding="utf-8")
    data = f.read()
    f.close()
    mt = MeCab.Tagger("-Owakati")

    wordlist = mt.parse(data)
    wordlist = wordlist.rstrip(" \n").split(" ")
    markov = {}
    w = ""

    #Markov Chain
    for x in wordlist:
        if w:
            if w in markov: 
                new_list = markov[w]
            else:
                new_list =[]
 
            new_list.append(x)
            markov[w] = new_list
        w = x

    choice_words = wordlist[binomial(n=30, p=0.5)] 
    sentence = ""
    count = 0
    tweet_length = binomial(n=30, p=0.5) + 1 #二項分布 + 1
    print("tweet_length:",tweet_length)
    while count < tweet_length:
            sentence += choice_words
            choice_words = random.choice(markov[choice_words])
            count += 1
 
            sentence = sentence.split(" ", 1)[0]
            p = re.compile("[!-/:-@[-`{-~]")
            sus = p.sub("", sentence)

    #半角英数字を除去する場合,正規表現
    words = re.sub(re.compile("[!-~]"),"",sus)

    #ツイートしたら面倒なワードは削除しとく
    sus.replace("plzww2","").replace("plze","").replace("plzbo3","") 
    print(sus)


    ############  ツイート実行部分  ##############
    params = {"status": sus}#{"status": "ツイート本文"}
    req = tw.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
    if req.status_code == 200: #req.status_codeが200だと正常終了している
            print ("Success! Your Tweet")
    else:
            print (req.status_code)
            
            
      
if __name__ == '__main__':
    DataCollect()
    SentenceGenerate()