#Dependancies
from flask import Flask, jsonify, render_template, request, redirect
import scrape_mars
import pymongo

app = Flask(__name__)

#Connecting to Mongodb

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars
mars = db.mars

#  create route that renders index.html template
@app.route('/')
def index():
    mars_info = db.mars.find_one()
    
    return render_template("index.html", mars_info=mars_info)


@app.route('/scrape')
def scrape():
    mars_info = db.mars
    mars_content = scrape_mars.scrape()
    mars_info.insert(
        {},
        mars_content,
        upsert=True
        )
    return index()

if __name__ == "__main__":
    app.run(debug=False)
