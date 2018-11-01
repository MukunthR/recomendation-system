
# coding: utf-8

# # BIA-660 Web Mining Project
# ## Web Scraping  Goodreads Website
# ## Project Title : Recommendation System
# 
# ![alt text](http://alexabloom.com/wp-content/uploads/2017/04/Goodreads-icon.png "Logo Title Text 1")
# 
# ### The link for the website: [www.goodreads.com](https://www.goodreads.com/list/tag/)
# ### Objectives: 
# Our project for BIA-660 Web Mining is going to focus on "Goodreads Books". We started this project to solve both a Business problem as well as to satisfy the user needs. This project focuses on the following:
# *	Categorizing the books using the classification methods (Naive Bayes, Support vector machine (SVM) & KNN), when a new book is added to the database, our model predicts which category the book belongs to.
# *	Recommending books to the user based on the user reviews (Category Based - Review Based).
# 
# 

# ## Scraping the tags (Categories) & Links
# Initally, we are scraping the 29 tags (categories of the books) and their links to go inside each category and browse for the books which belong to that category.
# * Using BeautifulSoup to scrape the data from the Goodreads website. 
# * Using "Request" library to retrive the source code.
# * Initializing a function called "getCategoryHref" to get the Cetegory links.
# * Writing the contents to the "categoryListGR.csv" File.
# 
# [categoryListGR.csv](https://github.com/MukunthR/recomendation-system/blob/master/categoryListGR.csv)

# In[ ]:


import requests
import csv
import pandas as pd

# import BeautifulSoup from package bs4 (i.e. beautifulsoup4)
from bs4 import BeautifulSoup

headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                          '86 Safari/537.36'}

page = requests.get('https://www.goodreads.com/list/tag/', headers = headers)

# send a get request to the web page
siteUrl = "https://www.goodreads.com"
category = {}

def getCategoryHref(url):
    page = requests.get(url, headers = headers)
    if page.status_code == 200:
        # initiate a beautifulsoup object using the html source and Python’s html.parser
        soup = BeautifulSoup(page.content, 'html.parser')
        hrefTag = soup.select('div#topRow > div.cell a.listTitle')
        for href in hrefTag:
            finalHref = siteUrl + href['href']
            break
        return finalHref    

if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
#     print(soup.prettify())
    categoryNameTags = soup.select('div ul.listTagsTwoColumn li a.actionLinkLite')
    for name in categoryNameTags:
        print(name)
        categoryHref = getCategoryHref(siteUrl + name['href'])
        category[name.text.strip()] = categoryHref
    
    with open('categoryListGR.csv', 'w') as file:
        wrt = csv.writer(file, delimiter=',', lineterminator='\n')
        wrt.writerow(['Category', 'Link'])
        for key,value in category.items():
            wrt.writerow([key,value])


# ## Fetching books from each category with their Scores and Links
# Each category from the previous step is called for and the data for the first 300 books are scrapped. This dataset includes Category, Names, Links and Scores attributes.
# * Creating a List each attribute and combining them to form Pandas Dataframe.
# * Using categoryListGR.csv file to fetch the data of the inidividual book. 
# * Writing the contents to the "categoryBookFile.csv" File.
# 
#  [categoryBookFile.csv](https://github.com/MukunthR/recomendation-system/blob/master/categoryBookFile.csv)

# In[ ]:


import requests
import csv
import pandas as pd

# import BeautifulSoup from package bs4 (i.e. beautifulsoup4)
from bs4 import BeautifulSoup

headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                          '86 Safari/537.36'}
BookName = []
bookLink = []
Page_No = []
bookTupList = []
Score = []
pairWiseScore = []
flagList = []
flagCount = 0
catCustom = []

siteUrl = "https://www.goodreads.com"
def pairwise(it):
    it = iter(it)
    while True:
        yield next(it), next(it)
        
def scrapeData(category, url):
    print(category)
    page = requests.get(url, headers = headers)
    if page.status_code == 200:
        
        print("page success")
        soup = BeautifulSoup(page.content, 'html.parser')
        bookName = soup.select('a.bookTitle span')
        for i in bookName:
            BookName.append(i.text)
            catCustom.append(category)
        link = soup.select('a.bookTitle')
        for i in link:
            bookLink.append(siteUrl + i['href'])
        scr = soup.select('div span.smallText > a')
        for i in scr:
            Score.append(i.text.strip())
        for a,b in pairwise(Score):
            pairWiseScore.append(a + b)
        flagList = list(zip(catCustom,BookName,bookLink,pairWiseScore))
        if (len(flagList) % 300) != 0:
            print(len(flagList))
            Page = soup.select('div.pagination a.next_page')
            if Page:
                for i in Page:
                    scrapeData(category, siteUrl + i["href"])
        return list(zip(catCustom,BookName,bookLink,pairWiseScore))
          

def scrapteCategoryData(categoryList):
    for category,categoryHref in categoryList.items():
        print(category,categoryHref)
        scrapeData(category, categoryHref)
        
    entireList = list(zip(catCustom,BookName,bookLink,pairWiseScore))
    for element in entireList:
        print(element)
    final_data = pd.DataFrame(entireList, columns = ['Category','Name','Link','Scores'])
    print(final_data)
    final_data.to_csv('categoryBookFile.csv', index = False)
    
    print("Total length is :: " + str(len(entireList)))


if __name__ == "__main__": 
    data = pd.read_csv("categoryListGR.csv", header=0)
    categoryList = dict(zip(data["Category"].values.tolist(), data["Link"].values.tolist()))
    scrapteCategoryData(categoryList)


# ## Getting the contents of the books
# The content of all the 300 books of each category is taken and stored in a csv file.
# *  Reading the entire csv file, fetch the movie links columns and convert it into list.
# * Iterate each movie links from the list and fetch book contents such as Name, Author Name, Author profile link, Ratings, Awards, Descriptions and which other category it belongs to.
# 
# [entireBookList1000.csv](https://github.com/MukunthR/recomendation-system/blob/master/entireBookList1000.csv)
# 
# [entireBookList8700.csv](https://github.com/MukunthR/recomendation-system/blob/master/entireBookList8700.csv)

# In[ ]:


import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup

headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                          '86 Safari/537.36'}

entireBookList = []

def scrapeData(link, category, score):
    OtherCategories = []
    page = requests.get(link, headers = headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        
        bookTag = soup.select('div h1#bookTitle')
        if not bookTag:
            bookName = "N/A"
        else:
            for tag in bookTag:
                bookName = tag.text.strip()
        
        authorTag = soup.select('div a.authorName')
        if not authorTag:
            authorName = "N/A"
        else:
            for author in authorTag:
                authorName = author.text.strip()
        
        authorLinkTag = soup.select('div a.authorName')
        if not authorLinkTag:
            authorLink = "N/A"
        else:
            for i in authorLinkTag:
                authorLink = i["href"]
        
        ratingTag = soup.select('span.average')
        if not ratingTag:
            rating = "N/A"
        else:
            for i in ratingTag:
                rating = i.text
        
        awardsTag = soup.select('div.infoBoxRowItem a.award')
        if not awardsTag:
            awards = 'N/A'
        else:
            for i in awardsTag:
                awards = i.text.strip()
        
        othrcat = soup.select('div.elementList a.actionLinkLite')
        if not othrcat:
            othrCat = "N/A"
        else:
            for i in othrcat:
                OtherCategories.append(i.text.strip())
            othrCat = " ".join(OtherCategories)
        
        
        descriptionTag = soup.select('div#description span')
        if not descriptionTag:
            description = "N/A"
        else:
            for i in descriptionTag:
                description = i.text
        
        
        bookTuple = (category, bookName, authorName, authorLink, rating, awards, othrCat, description,score)
        entireBookList.append(bookTuple)
        

if __name__ == "__main__":
    data = pd.read_csv("categoryBookFile.csv", header=0)
    movieLinkList = data["Link"].tolist()
    movieCategories = data["Category"].tolist()
    movieScores = data["Scores"].tolist()
    j = 0
    for link, category, score in zip(movieLinkList, movieCategories, movieScores):
        j += 1
        print(j)
        print(link, category, score)
        scrapeData(link, category, score)
        
    for element in entireBookList:
        print(element)
        
    final_data = pd.DataFrame(entireBookList, columns = ['Category','Book Name','Author Name','Author Link','Ratings', 'Awards', 'OtherLinks', 'Description', 'Score'])
    final_data.to_csv('entireBookList8700.csv', index = False)


# ## Lemmatization & Tokenization
# 

# In[ ]:


import nltk        
import string
from nltk.corpus import stopwords
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import re
import nltk
import numpy as np
import pandas as pd
# nltk.download('genesis')
# nltk.download('punkt')
# # # nltk.download('all')
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize
from scipy.spatial import distance
stop_words = stopwords.words('english')

# import string
wordnet_lemmatizer = WordNetLemmatizer()
lemmaAdj = []
lemmaVerb = []
tagged_tokens = []
token = []

# wordnet and treebank have different tagging systems
# define a mapping between wordnet tags and POS tags as a function
def get_wordnet_pos(pos_tag):
    # if pos tag starts with 'J'
    if pos_tag.startswith('J'):
        # return wordnet tag "ADJ"
        return wordnet.ADJ

    # if pos tag starts with 'V'
    elif pos_tag.startswith('V'):
        # return wordnet tag "VERB"
        return wordnet.VERB

    # if pos tag starts with 'N'
    elif pos_tag.startswith('N'):
        # return wordnet tag "NOUN"
        return wordnet.NOUN

    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        # be default, return wordnet tag "NOUN"
        return wordnet.NOUN
    
def tokenize(text):
#     print(text)
    token_count = None
    
    # converts the string into lowercase
#     for i in text:
#         low_text = i.lower()

    # segments the lowercased string into tokens - Based on the requirements
    pattern = r'[a-z0-9][a-z0-9-_.@]*[a-z0-9]'
    tokens = nltk.regexp_tokenize(text, pattern)

    # POS
    tagged_tokens= nltk.pos_tag(tokens)

    lemmatized_words=[wordnet_lemmatizer.lemmatize          (word, get_wordnet_pos(tag))           # tagged_tokens is a list of tuples (word, tag)
          for (word, tag) in tagged_tokens \
          # remove stop words
          if word not in stop_words and \
          # remove punctuations
          word not in string.punctuation]

    token_count = nltk.FreqDist(lemmatized_words)
    
    return token_count 

if __name__ == "__main__":

#     text=
    data = pd.read_csv("entireBookList1000.csv", header=0)
    text = data["Description"].tolist()
    
    tokenize(text)
    for key, value in tokenize(text).items():
        pass


# ## TF_IDF Matrix

# ## Graphs
