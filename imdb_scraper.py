# Created by: Ryan Vickramasinghe
# Scrapes IMDB to get latest TV shows and data

import requests
import csv
from bs4 import BeautifulSoup
from parsers import *

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

# This function will retrieve all the movie urls on the given search page, and add them to the data frame
def writeData(searchPageSoup, writer):
    # get urls for first movie
    urlList = getMovieUrlList(searchPageSoup)

    # get dictionary for each movie
    for url in urlList:
        movieData = scrapeMoviePage(url)
        for data in movieData:
            writer.writerow(data)

# This will scrape an IMDB tv show page for information and return a dictionary
def scrapeMoviePage(url):
    # fetch the live page
    page = getPage(url)

    # scrape the title
    title = scrapeTitle(page)

    # get keywords
    keywordsParsed = scrapeKeywords(page)

    # get genre
    genre = scrapeGenre(page)

    # check for both creators and stars
    creatorsParsed, starsParsed = scrapeCreatorsStars(page)

    # get rating
    rating = scrapeRating(page)

    # get details
    country, language, releaseYear, productionCosParsed = scrapeDetails(page)

    ## build the dictonary to return
    data = [{
        'title' : title,
        'keywords' : ' '.join(keywordsParsed),
        'genre' : genre,
        'creators' : ' '.join(creatorsParsed),
        'stars' : ' '.join(starsParsed),
        'rating' : rating,
        'country_of_origin' : country,
        'language' : language,
        'release' : releaseYear,
        'production_company' : ' '.join(productionCosParsed)
    }]
    return data


## DRIVER CODE

# headers
csv_cols = ['title', 'keywords', 'genre', 'creators', 'stars', 'rating',\
    'country_of_origin', 'language', 'release', 'production_company']

csv_file = "scraped_data.csv"
try:
    print('Opening file for writing...')
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
        writer.writeheader()
        print('Wrote header to file.')

        # get the first page
        searchUrl = 'https://www.imdb.com/search/title/?title_type=tv_series,tv_special,tv_miniseries,documentary,tv_short'
        soup = getPage(searchUrl)
        # get the toal number of results (so we know how many pages to crawl)
        numResults = getNumResults(soup)
        print('Total results: ', numResults)

        print('Processing page 1')
        writeData(soup, writer)

        currentSearchPage = 51
        numRuns = int(numResults) // 50
        if int(numResults) % 50 == 0:
            numRuns -= 1
        
        for i in range(numRuns):
            print('Processing page ' + str(i + 2))
            url = searchUrl + '&start=' + str(currentSearchPage)
            currentSearchPage += 50

            soup = getPage(url)
            writeData(soup, writer)

except IOError:
    print("I/O error")