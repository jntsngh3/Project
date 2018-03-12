#!/usr/bin/python# -*- coding: utf-8 -*-import requestsfrom bs4 import BeautifulSoupfrom tweepy import *import tweepyimport timeimport re#-------------------------------------------Connecting Twitter Account-----------------------------------------------------------print("Started Python Processing")config = {}exec(open("/Users/jayantsingh/Desktop/Project/src/extractor/script/config.py").read(), config)consumer_key = config["consumer_key"]consumer_secret = config["consumer_secret"]access_token = config["access_token"]access_token_secret = config["access_token_secret"]#-------------------------------------------Establishing Authentication-------------------------------------------------------------print ("Connecting to Twitter")auth = OAuthHandler(consumer_key, consumer_secret)auth.set_access_token(access_token, access_token_secret)api = tweepy.API(auth)trends1 = api.trends_place(23424975)#23424848#-------------------------------------------Extracting Trending Tweets-------------------------------------------------------------print ("Connection Successfull")open('/Users/jayantsingh/Desktop/Project/src/extractor/Trends.dat', 'w')open('/Users/jayantsingh/Desktop/Project/src/extractor/linkList.dat', 'w')tweets = []for location in trends1:    for trend in location["trends"]:        f =  open('/Users/jayantsingh/Desktop/Project/src/extractor/Trends.dat', 'a', encoding="utf8")        f.write("%s\n" % trend["name"].replace("#", '').replace(" ", "+"))        tweets.append("%s" % trend["name"].replace("#", '').replace(" ", "+"))#-------------------------------------------Extracting Amazon Links--------------------------------------------------------------# print (tweets)print ("Tweets Extracted succesfully")headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}links = []count = 0limit = 5for query in tweets:    time.sleep(1)    count += 1    if count >limit:        break    print(query)    r = requests.get('https://www.google.com/search?q=+'+query+'+amazon', headers=headers)    r.raise_for_status()    soup = BeautifulSoup(r.text, 'html.parser')    for item in soup.find_all('h3', attrs={'class' : 'r'}, limit=1):        links.append(item.a['href'])    print("Link "+str(count)+" extracted successfully")for link in links:    link.replace("?q=site:", "https://")r = re.compile("https://www.amazon.*")newLinks = filter(r.match, links)r = re.compile(".*dp.*")pureLinks = filter(r.match, newLinks)pLinks = []for link in pureLinks:    with open('/Users/jayantsingh/Desktop/Project/src/extractor/linkList.dat', 'a', encoding='utf8') as f:        f.write("%s\n" % link)        pLinks.append(link)        print(link)#-------------------------------------------------------------------------------------------------------------------------------------print ("Exited Python File")#------------------------------------------------DATA_EXTRACTION---------------------------------------------------------------------from lxml import htmldata = []for link in pLinks:    try:        context = requests.get(link)        parser = html.fromstring(context.content)        product_name = parser.xpath('//span[@id="productTitle"]/text()')[0]        product_name = product_name.strip()        prices = parser.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice") or contains(@class,"a-size-base a-color-price a-color-price") or contains(@class,"a-color-price")]/text()')        if len(prices)>1:            prices = [price for price in prices if not price.strip() == '']            fprice=prices[0]        else:            fprice=prices[0]        product_price = fprice.strip()        product_image = parser.xpath('//img[contains(@id,"landingImage") or contains(@id,"imgBlkFront")]/@src')[0]        product_image = product_image.strip()        dic = {            'product_link' : link ,            'product_name' : product_name ,            'product_price' : product_price,            'product_image' : product_image        }        data.append(dic)    except:        passprint(data)for dics in data:    print("PRODUCT_LINK " + dics["product_link"])    print("PRODUCT_NAME " + dics["product_name"])    print("PRODUCT_PRICE " + dics["product_price"])    print("PRODUCT_IMAGE " + dics["product_image"])    print()