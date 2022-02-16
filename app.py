from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)

host = os.environ.get("DB_URL")
client = MongoClient()
db = client.Premiere_PAL
# users = db.users
movie_colls = db.movie_coll
movies = db.movies

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/collections')
def collections():
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

@app.route('/overview')
def overview():
  return render_template('overview.html', movie=movie)

@app.route('/user')
def user():
  return render_template('user.html')

if __name__ == "__main__":
  app.run(debug=True)

