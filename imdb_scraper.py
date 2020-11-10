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
    title = title.split('\xa0', 2)[0].strip()

    # get keywords
    keywords = page.select('.itemprop')
    keywordsParsed = []
    for keyword in keywords:
        keywordsParsed.append(keyword.getText().strip())

    # get genre
    genre = page.select('.see-more.inline.canwrap')[1].select_one('a').getText().strip()

    # get creators
    creators = page.select('.credit_summary_item')[0].select('a')
    creatorsParsed = []
    for creator in creators:
        creatorsParsed.append(creator.getText().replace(' ', ',').strip())

    # get stars
    stars = page.select('.credit_summary_item')[1].select('a')
    starsParsed = []
    for star in stars:
        starsParsed.append(star.getText().replace(' ', ',').strip())
    del starsParsed[len(starsParsed) - 1] # remove the 'see full cast link'

    # get rating
    rating = page.find('span', itemprop='ratingValue').getText().strip()

    # get details
    detailsDiv = page.select_one('.article#titleDetails').select('div')
    country = detailsDiv[1].select_one('a').getText().strip()
    language = detailsDiv[2].select_one('a').getText().strip()
    releaseYear = detailsDiv[3].getText().split()[4]
    productionCos = detailsDiv[6].select('a')
    # parse production companies
    productionCosParsed = []
    for company in productionCos:
        companyText = company.getText().strip()
        if companyText != 'See more':
            productionCosParsed.append(companyText.replace(' ', ','))

    ## build the dictonary to return
    data = {
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
    }
    return data

# get the first page
soup = getPage('https://www.imdb.com/search/title/?title_type=tv_series,tv_special,tv_miniseries,documentary,tv_short')
# get the toal number of results (so we know how many pages to crawl)
numResults = getNumResults(soup)
print('Total results: ', numResults)

# get urls for first movie
urlList = getMovieUrlList(soup)

# get dictionary for each movie
for url in urlList:
    movieData = scrapeMoviePage(url)
    print(movieData)