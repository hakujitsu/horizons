from flask import Flask
from flask import request
from gnews import getSimilarArticles

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/scrape", methods=["POST"])
def scrape():
    assert request.path == '/scrape'
    assert request.method == 'POST'
    data = request.json
    print(data.get("url"))
    getSimilarArticles(data.get("url"))
    return "<p>Hello, World!</p>"