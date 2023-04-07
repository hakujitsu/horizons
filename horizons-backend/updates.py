# Imports the Google Cloud client library
from google.cloud import language_v1

# Based on AllSides Media Bias ratings
MEDIA_BIAS_RATINGS = {
    'ap': -1.5,
    'bbc': -0.8,
    'cnbc': -0.9,
    'cnn': -3.8,
    'fox': 4,
    'guardian': -2.4,
    'new_york_post': 1.8,
    'newsweek': 0.5,
    'pbs': -1.1,
    'reuters': 0,
    'washington_examiner': 2.3,
}

# Since all of the sources are non-Asian, no specific sources are recommended for the asian region.
LOCALE_BASED_RECS = {
    'america': ['bbc', 'guardian', 'reuters'],
    'europe': ['ap', 'cnbc', 'cnn', 'fox', 'new_york_post', 'newsweek', 'pbs', 'washington_examiner'],
}

"""
Analyses the entity sentiment of a given text.

Parameters:
    text_content: The text to analyse
"""
def analyze_entity_sentiment(text_content):
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.types.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    return response

"""
When a reader reads an article, their respective entity-sentiment scores will be updated. (Only entities of type PERSON, LOCATION, ORG and EVENT will be tracked)

Parameters:
    user_background: Dictionary with entities as keys and their corresponding sentiment as values.
    article_responses: Contains the various entities and their respective sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
"""
def update_opinion(user_background, article_responses):
    relevant_entities = ['PERSON', 'LOCATION', 'ORG', 'EVENT']

    for article_entity in article_responses.entities:
        article_entity_type = language_v1.Entity.Type(article_entity.type_).name

        if (article_entity_type in relevant_entities and article_entity in user_background[article_entity]):
            num_of_read_articles = user_background[article_entity][1]
            curr_sentiment = user_background[article_entity][0]

            new_sentiment = ((curr_sentiment * num_of_read_articles) + (article_entity.salience * article_entity.sentiment.score)) / float(num_of_read_articles + 1)

            user_background[article_entity][0] = new_sentiment
            user_background[article_entity][1] = num_of_read_articles + 1

"""
When a reader reads an article, their political bias scores will be updated. Returns the new political bias score for the given user.

Parameters:
    user_political_bias: The user's current political bias, measured based on the user's initial declaration (if any) and the accumulatation of all the articles read by the user. In the form of (baseline_bias, change, num_of_articles_read)
    curr_source_bias: The media bias rating (Taken from AllSides)
"""
def update_political_bias(user_political_bias, curr_source_bias):
    baseline_bias = user_political_bias[0]
    change = user_political_bias[1]
    num_of_articles_read = user_political_bias[2]

    new_change = ((change * num_of_articles_read) + curr_source_bias) / (num_of_articles_read + 1)

    return (baseline_bias, new_change, num_of_articles_read + 1)

# TODO: Compose the above 2 functions
def read_article():
    pass