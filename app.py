from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)

host = os.environ.get("DB_URL")
client = MongoClient()
db = client.Premiere.PAL
# users = db.users
collections = db.collections
movies = db.movies

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/collections')
def collections():
  return render_template('collections.html')

movie = {'title': 'Frozen', 'overview': 'abcd', 'release_date': 'November 27, 2013', 'poster_path': '/1eQ3c443YwXz1Xq0FZ24qrJBKyd.jpg', 'genre_ids': '[53, 80]'}

@app.route('/overview')
def overview():
  return render_template('overview.html', movie=movie)

@app.route('/user')
def user():
  return render_template('user.html')

if __name__ == "__main__":
  app.run(debug=True)

