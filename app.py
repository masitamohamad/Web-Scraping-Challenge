from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

###########################################################################################
# Flask Setup
###########################################################################################

app = Flask(__name__)

###########################################################################################
# Use PyMongo to establish Mongo connection
###########################################################################################

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

###########################################################################################
# Flask Routes
###########################################################################################
# Route to render index.html template using data from Mongo

@app.route("/")
def home():
  
    mars_data_dict = mongo.db.mars_data_dict.find_one()
    return render_template("index.html", mars_data_dict=mars_data_dict)

###########################################################################################
# Route that will trigger the scrape function

@app.route("/scrape")
def scraper():

    mars_data_dict = mongo.db.mars_data_dict

    # Run the scrape function from scrape_mars.py
    mars_data_update = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data_dict.update({}, mars_data_update, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)

###########################################################################################
# Main Behavior
###########################################################################################

if __name__ == "__main__":
    app.run(debug=True)