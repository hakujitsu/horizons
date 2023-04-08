from flask import Flask, request, jsonify
from gnews import getSimilarArticles
from users import addUserToDict
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/signup", methods=["POST"])
def sign_up():
    assert request.path == '/signup'
    assert request.method == 'POST'
    data = request.json
    age = data.get("age")
    location = data.get("location")
    politics = data.get("politics")
    id = addUserToDict(age, location, politics)
    return jsonify(
        user_id=id
    )

@app.route("/scrape", methods=["POST"])
@cross_origin()
def scrape():
    assert request.path == '/scrape'
    assert request.method == 'POST'
    data = request.json
    # user_id = data.get("user_id")
    # updateUserHistory(user_id, url)
    url = data.get("url")
    print("called scrape")
    print(url)
    getSimilarArticles(url)
    list = [
            {
                "title": "Communities face major destruction after large tornadoes tear through the South and Midwest, leaving at least 22 dead",
                "source": "CNN",
                "url": "https://edition.cnn.com/2023/04/02/us/us-severe-storm-south-midwest-sunday/index.html"
            },
            {
                "title": "Finland begins voting in knife-edge election",
                "source": "The Guardian",
                "url": "https://www.theguardian.com/world/2023/apr/02/finland-begins-voting-in-knife-edge-election"
            },
            {
                "title": "US tornadoes: Death toll grows as extreme storms ravage several states",
                "source": "BBC",
                "url": "https://www.bbc.com/news/world-us-canada-65150138"
            }
           ]
    return jsonify(recommendations = list, id = url)