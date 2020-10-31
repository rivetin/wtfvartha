from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
import time
import pymongo
import datetime
from pprint import pprint
from pymongo import MongoClient



TOKEN = os.getenv('TOKEN')
MONGOURL = os.getenv('MONGOURL')


client = pymongo.MongoClient(MONGOURL)

URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
def get_update():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js
def get_chat_id_and_text(updates):
    now = datetime.datetime.now()
    chat_list = []
    for i in updates['result']:
        if i['message']['chat']['id'] not in chat_list:
            chat_list.append(i['message']['chat']['id'])
            
    print("######################################################################")
    print("""\
 _ _ _ ___ ___   _ _           _    _       
| | | |_ _| __> | | |___ _ _ _| |_ | |_ ___ 
| | | || || _>  | ' <_> | '_> | |  | . <_> |
|__/_/ |_||_|   |__/<___|_|   |_|  |_|_<___| by Athul
                                            
""")
    print("######################################################################")
    print()
    print("Loading chat ids.......")
    print()
    for i in chat_list:
        print("chat id -> ",i)
    print()
    news_text = get_news_text()
    return (news_text, chat_list)

def get_news_text():
    now = datetime.datetime.now()
    url = ('https://newsapi.org/v2/top-headlines?''country=in&''apiKey=YOUR API KEY')
    print()
    print("Getting news json form -> \n\b",url)
    print()
    print("######################################################################")
    

    news = requests.get(url).json()
    article= news['articles']
    news_list = [u'\u2705 WTFVartha Headlines \n',now.strftime("%Y-%m-%d"),now.strftime("%H:%M")]
    for i in article:
        news_list.append(i['title']+"\n")
    text = u"\n\u23E9 "
    text = text.join(news_list)
    news_text = text
    return (news_text)
    

    

    


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    js=get_json_from_url(url)
    if js['ok'] == True:
        print("message sent to",chat_id)
        print()
    else:
        print ("messege failed to sent : ",js['description'])
        print()
    
def main():
    while True:
        text, chat_list = get_chat_id_and_text(get_update())
        for chat_i in chat_list:
            print("Trying to sent message to chat id ->" ,chat_i)
            send_message(text, chat_i)
            send_message("\u2705", chat_i)

        break

        


if __name__ == '__main__':
    main()


#https://api.telegram.org/bot<YourBOTToken>/getUpdates
#https://www.rapidtables.com/code/text/unicode-characters.html          (emoji link)

