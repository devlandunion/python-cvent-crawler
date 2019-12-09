import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import math
import csv
import re
import os
import pandas as pd

baseUrl = "https://www.cvent.com"

def getHtml(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)

    return html

def getImgLinks(url):
    try:
        html = getHtml(url)
        bsObject = BeautifulSoup(html, "lxml")
        imgContainer = bsObject.find('div', {'id':'carousel-thumbnails'})
        imgLinks = []

        if(imgContainer != None):
            for imgTag in imgContainer.find('div', {'role':'listbox'}).select('img'):
                imgLink = imgTag.get('src').replace('160/90', '780/437')
                imgLinks.append(imgLink)
    except:
        imgLinks = []
    
    return imgLinks

def downloadImages(directory, url):
    imgLinks = getImgLinks(url)

    if(len(imgLinks)):
        for index, link in enumerate(imgLinks):
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(link, directory + '/' + str(index) + '.jpg')
            except:
                print('image not downloadable')

        return len(imgLinks)
    else:
        return len(imgLinks)

def getDetails(url):
    html = getHtml(url)
    bsObj = BeautifulSoup(html, "lxml")
    details = {}

    details['name'] = bsObj.find('h1', {'itemprop':'name'}).text.strip()
    details['address'] = bsObj.find('span', {'itemprop':'address'}).text.strip()

    for key in details:
        print(key)
        print(details[key])

def main():
    targetUrl = 'https://www.cvent.com/venues/orlando/hotel/rosen-shingle-creek/venue-c1c0927e-a603-4541-9109-fde9b1f0c47e'
    # directory = './hotel_data/images/'
    # downloadImages(directory, targetUrl)
    getDetails(targetUrl)

if __name__ == '__main__':
    main()