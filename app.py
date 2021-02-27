from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from scrape_mars import scrape

# Create an instance of Flask
app = (__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_db=mars_info)

# Import scrape_mars.py script 
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()




 