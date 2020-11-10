# Created by: Ryan Vickramasinghe
# This class holds parsing functions for processing scraped data

from bs4 import BeautifulSoup

def scrapeTitle(page):
    title = page.select_one('.title_wrapper') \
        .select_one('h1').getText()
    title = title.split('\xa0', 2)[0].strip()

    return title

def scrapeKeywords(page):
    keywords = page.select('.itemprop')
    keywordsParsed = []
    for keyword in keywords:
        keywordsParsed.append(keyword.getText().strip())

    return keywordsParsed

def scrapeGenre(page):
    return page.select('.see-more.inline.canwrap')[1].select_one('a').getText().strip()

def scrapeKeywordsGenre(page):
    keywordsParsed = []
    genre = ''

    storylineDiv = page.select('.see-more.inline.canwrap')
    for div in storylineDiv:
        header = div.select_one('h4')
        if (header == None):
            continue
        else:
            header = header.getText().strip()

        if (header == 'Plot Keywords:'):
            keywords = div.select('.itemprop')
            for keyword in keywords:
                keywordsParsed.append(keyword.getText().strip())
        elif (header == 'Genres:'):
            genre = div.select_one('a').getText().strip()

    return keywordsParsed, genre

def scrapeCreatorsStars(page):
    creatorStars = page.select('.credit_summary_item')
    creatorsParsed = []
    starsParsed = []
    for item in creatorStars:
        header = item.select_one('h4').getText().strip()
        if(header == 'Creators:' or header == 'Director'):
            # get creators
            creators = item.select('a')
            for creator in creators:
                creatorsParsed.append(creator.getText().replace(' ', ',').strip())
        elif (header == 'Stars:'):
            # get stars
            stars = item.select('a')
            for star in stars:
                starsParsed.append(star.getText().replace(' ', ',').strip())
            del starsParsed[len(starsParsed) - 1] # remove the 'see full cast link'
    
    return creatorsParsed, starsParsed

def scrapeRating(page):
    ratingItem = page.find('span', itemprop='ratingValue')
    rating = ''
    if ratingItem:
        rating = ratingItem.getText().strip()
    
    return rating

def scrapeDetails(page):
        detailsDiv = page.select_one('.article#titleDetails').select('div')

        country = ''
        language = ''
        releaseYear = ''
        productionCosParsed = []

        for div in detailsDiv:
            header = div.select_one('h4')
            if (header == None): 
                continue
            else:
                header = header.getText().strip()

            if (header == 'Country:'):
                country = div.select_one('a').getText().strip()
            elif (header == 'Language:'):
                language = div.select_one('a').getText().strip()
            elif (header == 'Release Date:'):
                releaseYear = div.getText().split()[4]
            elif (header == 'Production Co:'):
                productionCos = div.select('a')
                # parse production companies
                productionCosParsed = []
                for company in productionCos:
                    companyText = company.getText().strip()
                    if companyText != 'See more':
                        productionCosParsed.append(companyText.replace(' ', ','))

        return country, language, releaseYear, productionCosParsed