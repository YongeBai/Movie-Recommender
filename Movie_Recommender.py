import requests
import json

def get_movies_from_tastedive(movie):
    baseurl = 'https://tastedive.com/api/similar'
    param_d = {}
    param_d['q'] = movie
    param_d['type'] = 'movies'
    param_d['limit'] = 5
    resp = requests.get(baseurl, param_d)
    
    return resp.json()

def extract_movie_titles(diction):
    titles = [title['Name'] for title in diction['Similar']['Results']]
    return titles

def get_related_titles(lst):
    new_lst = []
    
    titles = []
    for movie in lst:
        titles.append(extract_movie_titles(get_movies_from_tastedive(movie)))
        
    for i in titles:
        for movie in i:
            if new_lst.count(movie) == 0:
                new_lst.append(movie)
           
    return new_lst

def get_movie_data(movie):
    baseurl = 'http://www.omdbapi.com/'
    parama_d = {}
    parama_d['t'] = movie
    parama_d['r'] = 'json'
    resp = requests.get(baseurl, parama_d)
    
    return resp.json()

def get_movie_rating(diction):
    
    rating = ''
    
    for i in diction['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            rating = i['Value']
            rating = int(rating.replace('%', ''))
            return rating
    return 0
        
def get_sorted_recommendations(lst):
    movies = get_related_titles(lst)
    
    scores = []
    titles = []
    
    for movie in movies:
        scores.append(get_movie_rating(get_movie_data(movie)))
        titles.append(movie)
     
    return [movies for (ratings,movies) in sorted(list(zip(scores,titles)),reverse = True)]
    