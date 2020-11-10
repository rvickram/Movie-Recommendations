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

# This function gets all the movies on a page
def getMovieUrlList(soupPage):
    divList = soupPage.select('.lister-list .mode-advanced')
    urls = []
    for div in divList:        
        # titleLink = div.find_all('a', href=True)[0]['href']
        titleLink = div.select_one('.lister-item-header').select_one('a')['href']
        urls.append('https://www.imdb.com' + titleLink)
    return urls

# This will scrape an IMDB tv show page for information and return a dictionary
def scrapeMoviePage(url):
    # fetch the live page
    page = getPage(url)

    # scrape the title
    title = page.select_one('.title_wrapper') \
        .select_one('h1').getText()
    # clean the title
    title = title.split('\xa0', 2)[0]

    # get keywords
    keywords = page.select('.itemprop')
    keywordsParsed = []
    for keyword in keywords:
        keywordsParsed.append(keyword.getText())

    data = {
        'title' : title,
        'keywords' : keywordsParsed
    }
    return data

# get the first page
soup = getPage('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries,documentary,tv_short&languages=en&ref_=adv_prv')
# get the toal number of results (so we know how many pages to crawl)
numResults = getNumResults(soup)
print('Total results: ', numResults)

# get urls for first movie
urlList = getMovieUrlList(soup)

# get dictionary for each movie
for url in urlList:
    movieData = scrapeMoviePage(url)
    print(movieData)