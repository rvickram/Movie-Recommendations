# Movie Recommendations
 A Python machine learning project I did which will make movie recommendations using real data scraped from IMDB!
 
## Model
The underlying model uses the following features (each weighted differently):

- Genres
- Plot
- Synopsis
- Cast
- Production company
- Keywords (describing the show)
- Number of seasons
- Episode runtime
- IMDB Rating
- Metacritic score
- Metacritic user score
- Using these, the model finds pairwise cosine_similarities between every TV Show in the database. Combining the top 30 most similar with a weighted average of IMDB and metacritic scores gives an overall recommendation score.

## Web Scraper
The web scraper uses the BeautifulSoup python library. It parses data to a CSV file, which is then used by the machine learning process.
