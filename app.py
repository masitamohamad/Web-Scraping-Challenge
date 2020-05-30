from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

###########################################################################################
# Flask Setup
###########################################################################################

app = Flask(__name__)

###########################################################################################
# Database Setup: Use flask_pymongo to set up connection
###########################################################################################

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

###########################################################################################
# Flask Routes
###########################################################################################

@app.route("/")
def home():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_info)

###########################################################################################
# Define what to do when a user hits the "/scrape" route

@app.route("/scrape")
def scraper():

    # Run the scrape function from scrape_mars.py
    mars_data_dict = scrape_mars.scrape()

    # Update mongo database
    mongo.db.collection.update({}, mars_data_dict, upsert=True)
    
    # Redirect to the home page
    return redirect("/", code=302)

###########################################################################################
# Main Behavior
###########################################################################################

if __name__ == "__main__":
    app.run(debug=True)

