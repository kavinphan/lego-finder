from flask import Flask, render_template, request
from dotenv import load_dotenv
from rebrickable import get_sets, get_set
from scrapers import scrape_amazon, scrape_ebay

app = Flask(__name__)

load_dotenv()

# Landing page with the search input
@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

# Search results page with links to sets
@app.route("/search", methods=['POST'])
def search():
    search = request.form['search']
    
    results = get_sets(search)

    return render_template('search.html', search=search, results=results)

# Set page to show a lego set and the scraped information
@app.route("/set/<id>", methods=['GET'])
def set(id):
    set = get_set(id)
    amazon_results = scrape_amazon(id)
    ebay_results = scrape_ebay(id)

    return render_template('set.html', set=set, amazon_results=amazon_results, ebay_results=ebay_results)
