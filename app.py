from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from forms import SearchForm
import requests
import os
import bcrypt

API_KEY = os.getenv('API_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

host = os.environ.get("DB_URL")
client = MongoClient()
db = client.Premiere_PAL
users = db.users
movie_colls = db.movie_coll
movies = db.movies

def create_title_str(title):
  title = title.split()
  title_str = ''
  for i in range(len(title)):
    if i == 0:
      title_str += title[i]
    else:
      title_str += f'+{title[i]}'
  return title_str

def get_movie_details(title_str):
  response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title_str}')
  response_data = response.json()
  
  movie_id = response_data['results'][0]['id']
  
  details = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos')
  movie = details.json()
  return movie

# Login & Register
@app.route('/login')
def login_index():
    if 'email' in session:
        return redirect(url_for('home'))
    
    return render_template('login_index.html')

@app.route('/signin', methods=['POST'])
def signin():
    login_user = users.find_one({'email' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['email'] = request.form['email']
            session['name'] = login_user['name']
            return redirect(url_for('login_index'))
    flash('Invalid email/password combination')
    return render_template('login_index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'email' : request.form['email'], 'password' : hashpass })
            session['email'] = request.form['email']
            return redirect(url_for('login_index'))
        
        flash('That email already exists!')
        return render_template('login_register.html')
    
    return render_template('login_register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    #session.pop('name', None)
    return redirect(url_for('login_index'))

@app.route('/')
def index():
  response = requests.get(f'https://api.themoviedb.org/3/trending/all/day?api_key={API_KEY}')
  results = response.json()
  return render_template('index.html', results = results['results'])

@app.route('/home')
def home():
  response = requests.get(f'https://api.themoviedb.org/3/trending/all/day?api_key={API_KEY}')
  results = response.json()
  return render_template('home.html', results = results['results'])

@app.route('/search', methods=['POST'])
def search():
  form = SearchForm()
  post_data = form.search.data
  title = create_title_str(post_data)
  response = requests.get(f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&page=1&query={title}&include_adult=false')
  response_data = response.json()
  results = response_data['results']

  return render_template("search.html", results=results )

@app.route('/collections')
def collections():
  user = users.find_one({"email": session.get("email")})
  user_collections = list(movie_colls.find({"user": user["_id"]}))
  return render_template('collections.html', collections=user_collections)

@app.route('/collections/new')
def collections_new():
  return render_template('new-collection.html', title='New Collection', collection ={})

@app.route('/collections', methods=['POST'])
def collections_submit():
  user = users.find_one({"email": session.get("email")})
  collection = {
    'user': user['_id'],
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'movies': []
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

@app.route('/overview/<movie_title>')
def overview(movie_title):
  title_str = create_title_str(movie_title)
  movie = get_movie_details(title_str)
  video_id = movie['videos']['results'][0]['id']
  genres = []
  for genre in movie['genres']:
    genres.append(genre['name'])
  return render_template('overview.html', movie=movie, genres=genres, video_id=video_id)

@app.route('/movie/<movie_title>/collections')
def choose_collection(movie_title):
  title_str = create_title_str(movie_title)
  movie = get_movie_details(title_str)
  user = users.find_one({"email": session.get("email")})
  user_collections = list(movie_colls.find({"user": user["_id"]}))
  
  return render_template('choose_collection.html', movie=movie, collections=user_collections)

@app.route('/movie/<movie_title>/collections/<collection_id>', methods=['GET', 'POST'])
def add_movie(movie_title, collection_id):
  title_str = create_title_str(movie_title)
  movie = get_movie_details(title_str)

  collection = movie_colls.find_one({'_id': ObjectId(collection_id)})
  movies = collection['movies']
  movies.append(movie)
  
  update_movies = {
    'movies': movies
  }
  movie_colls.update_one(
    {'_id': ObjectId(collection_id)},
    {'$set': update_movies})
  
  return render_template('collection_show.html', collection=collection)

@app.route('/user')
def user():
  user = users.find_one({"email": session.get("email")})
  user_collections = list(movie_colls.find({"user": user["_id"]}))
  return render_template('user.html', collections=user_collections)

if __name__ == "__main__":
  app.run(debug=True)

