from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    
    #  Find one record of data from the mongo db
    mars_db = mongo.db.mars_db.find_one()
    
    # Return template and data
    return render_template("index.html", mars_db=mars_db)


@app.route("/scrape")
def scrape():
    
    mars_db = mongo.db.mars_db
    
    # Scrape data
    mars_data = scrape_mars.scrape()
    
    # Update mars_info db 
    mars_db.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)





 