from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.Premiere-PAL
# users = db.users
collections = db.collections
movies = db.movies

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/collections')
def collections():
  return render_template('collections.html')

if __name__ == "__main__":
  app.run(debug=True)

