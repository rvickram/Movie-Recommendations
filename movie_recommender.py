import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Helper functions
def get_title_from_index(data, index):
	return data[data.index == index]["title"].values[0]

def get_index_from_title(data, title):
	return data[data.title == title]["index"].values[0]
##################################################

## Read CSV file
df = movieData = pd.read_csv('./data/movie_dataset.csv')
print(df.head())

## Select features
features = ['keywords', 'cast', 'genres', 'director']
# clean out NaN values in features
for feature in features:
	df[feature] = df[feature].fillna('')

## Combine the features into a single string
def combine_features(row):
	return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
# create new column with combined features
df['combined_features'] = df.apply(combine_features, axis=1) # axis=1 means pass rows not columns
print(df['combined_features'].head())

## Create count matrix from this new combined column
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['combined_features'])

## Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)

## function to retrieve a list of similar movies
def getSimilarMovie(data, movie_title, cosine_simulation):
	movie_index = get_index_from_title(data, movie_title)

	# get list of tuples
	similar_movies = list(enumerate(cosine_simulation[movie_index]))

	# sort to find the most relevant (in descending order)
	sorted_similar_movies = sorted(similar_movies, key=lambda x : x[1], reverse=True)
	top50_sorted = sorted_similar_movies[:50]

	# get a titles from the indexes in tuples
	recommendations = []
	scores = []
	for movie in top50_sorted:
		recommendations.append(get_title_from_index(data, movie[0]))
		scores.append(movie[1])
	# remove the first score (since it will be the movie recommendations are based on)
	del recommendations[0]
	del scores [0]
	
	return recommendations, [element * 100 for element in scores]

## Test the movie
top50, scores = getSimilarMovie(df, 'Avatar', cosine_sim)

print('Top 50:\n', top50)
print('\nScores:\n', scores)