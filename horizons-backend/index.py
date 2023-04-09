from flask import Flask, request, jsonify
from gnews import getSimilarArticles, scrapeOriginalArticle
from users import addUserToDict
from flask_cors import CORS, cross_origin
from users import updateUserHistory, getUserFromDict, addMockUserToDict
from recommendation import get_final_recommendations
from updates import read_article
from shortlist_headlines import headline_similarity_score

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
    email = data.get("email")
    location = data.get("location")
    politics = data.get("politics")
    id = addUserToDict(email, location, politics)
    return jsonify(
        user_id=id
    )

@app.route("/scrape", methods=["POST"])
@cross_origin()
def scrape():
    assert request.path == '/scrape'
    assert request.method == 'POST'
    data = request.json
    user_id = data.get("user_id")["user_id"]
    url = data.get("url")
    print(url)
    # print(user_id)

    # TODO: remove later
    # user_id = 0
    # addMockUserToDict()

    updateUserHistory(user_id, url)
    user = getUserFromDict(user_id)

    original_article = scrapeOriginalArticle(url)
    # Article could not be scraped.
    if (original_article == None):
        return jsonify(recommendations = [], id = url)

    read_article(user, original_article)
    articles = getSimilarArticles(original_article)

    print(original_article.title)
    print(len(articles))

    # TODO: consider other methods of shortlisting
    # score_list = map(lambda a: headline_similarity_score(original_article.title, a.title), articles)
    # print(list(score_list))
    # articles = articles[0:10]

    recommendations = get_final_recommendations(user, original_article, articles)
    print(recommendations)

    recs = list(map(lambda r: r.export(), recommendations))

    return jsonify(recommendations = recs, id = url)