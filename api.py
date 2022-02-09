import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
word = os.environ.get('random_word')
print(word)
print(API_KEY)
# def search():
#     SEARCH_BASE = 'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query='
#     movie = input('Please enter the name of your movie: ').split()
#     query_str = ''


response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query=now+you+See+Me')
movie = response.json()
print(movie)
id = movie['results'][0]['id']
title = movie['results'][0]['original_title']

details = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}')
movie_details = details.json()

