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


@app.route('/user')
def user():
  return render_template('user.html')

if __name__ == "__main__":
  app.run(debug=True)

