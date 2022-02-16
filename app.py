from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import os

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)

host = os.environ.get("DB_URL")
client = MongoClient()
db = client.Premiere_PAL
<<<<<<< HEAD

# users = db.users
movie_coll = db.movie_coll
=======
# users = db.users
movie_colls = db.movie_coll
>>>>>>> 64888560ef3f4bab7084d22c29fd8de1594c856d
movies = db.movies

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/collections')
def collections():
<<<<<<< HEAD
  return render_template('collections.html')

movie = {'title': 'Frozen', 'overview': 'abcd', 'release_date': 'November 27, 2013', 'poster_path': '/1eQ3c443YwXz1Xq0FZ24qrJBKyd.jpg', 'genre_ids': [53, 80]}
=======
  return render_template('collections.html', collections=movie_colls.find())

@app.route('/collections/new')
def collections_new():
  return render_template('new-collection.html', collection ={})

@app.route('/collections', methods=['POST'])
def collections_submit():
  collection = {
    'title': request.form.get('title'),
    'description': request.form.get('description')
  }
  movie_colls.insert_one(collection)
  return redirect(url_for('collections'))

# Overview
movie = {'title': 'Frozen', 'overview': 'abcd', 'release_date': 'November 27, 2013', 'poster_path': '/1eQ3c443YwXz1Xq0FZ24qrJBKyd.jpg', 'genre_ids': '[53, 80]'}
>>>>>>> 64888560ef3f4bab7084d22c29fd8de1594c856d

@app.route('/overview')
def overview():
  response = requests.get(f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US')
  genre = response.json()
  ids = movie['genre_ids']
  genres = []
  for genre_id in ids:
    for genre_detail in genre['genres']:
      if genre_detail['id'] == genre_id:
        genres.append(genre_detail['name'])
    
  return render_template('overview.html', movie=movie, genres=genres)

@app.route('/user')
def user():
  return render_template('user.html')

if __name__ == "__main__":
  app.run(debug=True)

