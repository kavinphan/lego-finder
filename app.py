from flask import Flask, render_template, request
from dotenv import load_dotenv
from rebrickable import get_sets, get_set

app = Flask(__name__)

load_dotenv()

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
    search = request.form['search']
    
    results = get_sets(search)

    return render_template('search.html', search=search, results=results)

@app.route("/set/<id>", methods=['GET'])
def set(id):
    set = get_set(id)

    return render_template('set.html', set=set)
