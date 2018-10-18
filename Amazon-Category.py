import requests
import csv
import pandas as pd

# import BeautifulSoup from package bs4 (i.e. beautifulsoup4)
from bs4 import BeautifulSoup

page = requests.get('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=books')

# send a get request to the web page

if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
    categoryDictionary = {}
    categoryNames = []
    categoryLinks =[]
    categoryLinkTags = soup.select('div#leftNav > ul ul li > span a')
    categoryNameTags = soup.select('div#leftNav > ul ul span.a-size-small')
    for link in categoryLinkTags:
        categoryLinks.append(link)
    for name in categoryNameTags:
        categoryNames.append(name.text)


    if(len(categoryNames) == len(categoryLinks)):
        joinList = list(zip(categoryNames,categoryLinks))
        with open('categoryList.csv', 'w') as file:
            wrt = csv.writer(file, delimiter=',', lineterminator='\n')
            wrt.writerow(['Category', 'Link'])
            for i in range(len(joinList)):
                wrt.writerow(joinList[i])

