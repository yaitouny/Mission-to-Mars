from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
	# Run scraped function
	mars_app = mongo.db.mars
	mars_data = scrape_mars.scrape()

	mars_app.update({}, mars_data, upsert=True)
	return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
