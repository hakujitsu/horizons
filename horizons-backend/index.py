from flask import Flask, request, jsonify
from gnews import getSimilarArticles
from users import addUserToDict

app = Flask(__name__)

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
def scrape():
    assert request.path == '/scrape'
    assert request.method == 'POST'
    data = request.json
    # user_id = data.get("user_id")
    # updateUserHistory(user_id, url)
    url = data.get("url")
    getSimilarArticles(url)
    return "<p>Hello, World!</p>"