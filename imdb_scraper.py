# Created by: Ryan Vickramasinghe
# Scrapes IMDB to get latest TV shows and data

import requests
from bs4 import BeautifulSoup

# This function gets a BeautifulSoup object from a given url
def getPage(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# This function gets a count of results
def getNumResults(soupPage):
    description = soupPage.select('.desc')[0].getText()
    splitString = description.split()
    return splitString[2].replace(',', '')


# get the first page
soup = getPage('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries,documentary,tv_short&languages=en&ref_=adv_prv')
# get the toal number of results (so we know how many pages to crawl)
numResults = getNumResults(soup)


print(numResults)