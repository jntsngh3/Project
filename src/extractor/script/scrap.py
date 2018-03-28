from lxml import html
import csv, os, json
from time import sleep
import requests
from bs4 import BeautifulSoup
from tweepy import *
import tweepy
import re

#===================================================================================================================

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    urlData = requests.get(url, headers=headers)
    flag = True
    while flag is True:
        sleep(3)
        try:
            content = html.fromstring(urlData.content)

            productName = content.xpath('//h1[@id="title"]//text()')
            productSalesPrice = content.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()')
            productCategory = content.xpath('//a[@class="a-link-normal a-color-tertiary"]//text()')
            productOriginalPrice = content.xpath('//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()')
            productAvailability = content.xpath('//div[@id="availability"]//text()')
            productImage = content.xpath('//img[contains(@id,"landingImage") or contains(@id,"imgBlkFront")]/@src')

            NAME = ' '.join(''.join(productName).split()) if productName else None
            SALE_PRICE = ' '.join(''.join(productSalesPrice).split()).strip() if productSalesPrice else None
            CATEGORY = ' > '.join([i.strip() for i in productCategory]) if productCategory else None
            ORIGINAL_PRICE = ''.join(productOriginalPrice).strip() if productOriginalPrice else None
            AVAILABILITY = ''.join(productAvailability).strip() if productAvailability else None
            IMAGE = ''.join(productImage).strip() if productImage else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if urlData.status_code != 200:
                raise ValueError('captha')
                flag = False

            if NAME == None and SALE_PRICE == None and CATEGORY == None and ORIGINAL_PRICE == None and AVAILABILITY == None and IMAGE == None:
                print("Item not available")
                flag = False


            data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'AVAILABILITY': AVAILABILITY,
                'URL': url,
                'IMAGE': IMAGE
            }

            return data
        except Exception as e:
            print(e)


#==========================================================================================================


def exctraction():
    with open("Links.txt", 'r') as f:
        linksList = f.read().split("\n")
    linksList.remove('')
    print(linksList)
    extracted_data = []
    for i in linksList:
        url = i
        print("Processing: " + i)
        extracted_data.append(AmzonParser(url))
        sleep(3)
    for e in extracted_data:
        with open("d.txt", 'a', encoding="utf8") as rf:
            rf.write("%s\n" %e)
    fd = open('data.json', 'a')
    json.dump(extracted_data, fd, indent=4)


tweets = []


def TweetExtraction():
    # -------------------------------------------Connecting Twitter Account-----------------------------------------------------------
    print("Started Python Processing")
    config = {}
    exec(open("/Users/jayantsingh/Desktop/Project/src/extractor/script/config.py").read(), config)

    consumer_key = config["consumer_key"]
    consumer_secret = config["consumer_secret"]
    access_token = config["access_token"]
    access_token_secret = config["access_token_secret"]

    # -------------------------------------------Establishing Authentication-------------------------------------------------------------
    print("Connecting to Twitter")
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    trends1 = api.trends_place(23424975)
    # 23424848
    # 23424975

    # -------------------------------------------Extracting Trending Tweets-------------------------------------------------------------
    print("Connection Successfull")
    open('/Users/jayantsingh/Desktop/Project/src/extractor/Trends.dat', 'w')
    open('/Users/jayantsingh/Desktop/Project/src/extractor/linkList.dat', 'w')

    for location in trends1:
        for trend in location["trends"]:
            f = open('/Users/jayantsingh/Desktop/Project/src/extractor/Trends.dat', 'a', encoding="utf8")
            f.write("%s\n" % trend["name"].replace("#", '').replace(" ", "+"))
            tweets.append("%s" % trend["name"].replace("#", '').replace(" ", "+"))

#=======================================================================================================================


if __name__ == "__main__":
    TweetExtraction()
    open("Links.txt", 'w')
    open("data.json", 'w')
    open("d.txt", 'w')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
    headers1 = {'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'}
    count = 0
    limit = 5
    for searchString in tweets:
        count+=1
        if count>limit:
            break
        sleep(2)
        print(
            "Rquesting : " + "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=" + searchString)
        r = requests.get("http://www.amazon.com/s?url=search-alias%3Daps&field-keywords=" + searchString, headers)
        print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        r.raise_for_status()
        links = []
        for i in soup.find_all('a'):
            if i.get('href') is not None:
                links.append(i.get('href'))

        obj = re.compile(".*dp.*")
        obj2 = re.compile("https://www.amazon.*")
        dpRawLinks = filter(obj.match, links)
        dpRawLinks = filter(obj2.match, dpRawLinks)
        dpLinks = []
        for i in dpRawLinks:
            dpLinks.append(i)

        setDpLinks = set(dpLinks)
        clearDpLinks = [x.replace('#customerReviews', '').replace('#productPromotions', '').replace('&selectObb=rent', '') for x in setDpLinks]
        c = 0
        l = len(clearDpLinks)
        # print(l)
        c = 0
        l = 5
        for i in clearDpLinks:
            c += 1
            if c > l:
                break
            print(str(c) + " " + i)
            with open("Links.txt", 'a', encoding="utf8") as fs:
                fs.write("%s\n" % i)
    exctraction()
