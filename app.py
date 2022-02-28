from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from forms import SearchForm
import requests
import os

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

host = os.environ.get("DB_URL")
client = MongoClient()
db = client.Premiere_PAL
# users = db.users
movie_colls = db.movie_coll
movies = db.movies

def create_title_str(title):
  title_str = ''
  for i in range(len(title)):
    if i == 0:
      title_str += title[i]
    else:
      title_str += f'+{title[i]}'
  return title_str

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
  form = SearchForm()
  post_data = form.search.data
  title = create_title_str(post_data.split())
  response = requests.get(f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&page=1&query={title}&include_adult=false')
  response_data = response.json()
  results = response_data['results']

  return render_template("search.html", results=results )

@app.route('/collections')
def collections():
  return render_template('collections.html', collections=movie_colls.find())

@app.route('/collections/new')
def collections_new():
  return render_template('new-collection.html', title='New Collection', collection ={})

@app.route('/collections', methods=['POST'])
def collections_submit():
  collection = {
    'title': request.form.get('title'),
    'description': request.form.get('description')
  }
  movie_colls.insert_one(collection)
  return redirect(url_for('collections'))

@app.route('/collections/<collection_id>')
def collection_show(collection_id):
  collection = movie_colls.find_one({'_id': ObjectId(collection_id)})
  return render_template('collection_show.html', collection=collection)

@app.route('/collections/<collection_id>/edit')
def collection_edit(collection_id):
  collection = movie_colls.find_one({'_id': ObjectId(collection_id)})
  return render_template('collection_edit.html', collection=collection, title='Edit Collection')

@app.route('/collections/<collection_id>/delete', methods=['POST'])
def collection_delete(collection_id):
  movie_colls.delete_one({'_id': ObjectId(collection_id)})
  return redirect(url_for('collections'))

@app.route('/collections/<collection_id>', methods=['POST'])
def collection_update(collection_id):
  updated_collection = {
    'title': request.form.get('title'),
    'description': request.form.get('description')
  }
  movie_colls.update_one(
    {'_id': ObjectId(collection_id)},
    {'$set': updated_collection})
  return redirect(url_for('collection_show', collection_id=collection_id))

# Overview
movie = {'title': 'Frozen', 'overview': 'abcd', 'release_date': 'November 27, 2013', 'poster_path': '/1eQ3c443YwXz1Xq0FZ24qrJBKyd.jpg', 'genre_ids': '[53, 80]'}

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

