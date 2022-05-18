#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import lxml
from urllib.parse import urlparse
from urllib.parse import parse_qs
from google_play_scraper import app
import json
import datetime
import csv
import os
import sys

# baseurl  = "https://play.google.com/store/apps/category/ART_AND_DESIGN?hl=en&gl=us"
# baseurl = "https://play.google.com/store/apps/collection/cluster?clp=ogo5CAESD01VU0lDX0FORF9BVURJTxocChZyZWNzX3RvcGljX3lfUloteWtSbDRvEDsYAyoCCAdSAggC:S:ANO1ljKJICM&gsr=CjyiCjkIARIPTVVTSUNfQU5EX0FVRElPGhwKFnJlY3NfdG9waWNfeV9SWi15a1JsNG8QOxgDKgIIB1ICCAI%3D:S:ANO1ljLvuBk"
usage = '''scrapper.py [url to apps category] eg
scrapper.py "https://play.google.com/store/apps/category/ART_AND_DESIGN?hl=en&gl=us"
'''
try:
    baseurl  = sys.argv[1]
except IndexError:
    print(usage);exit()

appid = []
validapps = []
def excavator():
    soup = BeautifulSoup(requests.get(baseurl).content, "lxml")
    # print(soup.prettify())
    for link in soup.find_all(class_="wXUyZd"):
        url = link.find("a")["href"]
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)['id'][0]
        appid.append(captured_value)
        # App()
        # print(captured_value)

# extracts information about the app
def App():
    global result
    for application in appid:
        result = app(
            application,
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        if result["minInstalls"] >= 100000000:
            # validapps.append(app)
            print("Title: "+ result["title"])
            print("AppId: "+ result["appId"])
            print("url: "+ result["url"])
            print("Installs: " + result["installs"])
            print("minInstalls: " + str(result["minInstalls"]))
            print("Version: " + result["version"])
            print("updated: " + str( datetime.datetime.fromtimestamp(result["updated"]).strftime('%Y-%m-%d %H:%M:%S')))
            print("\n")
            export_to_csv()

def export_to_csv():
    fieldnames = ['Title', 'AppId', 'url', 'Installs','minInstalls','Version','updated']
    rows = [
    result["title"],
    result["appId"],
    result["url"],
    result["installs"],
    result["minInstalls"],
    result["version"],
    str(datetime.datetime.fromtimestamp(result["updated"]).strftime('%Y-%m-%d %H:%M:%S'))
    ]
    with open('playstore.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rows)
        print("file found writing data")


# TODO add category functionality(now)




if __name__ == '__main__':
    excavator()
    App()
