"""
This file includes all the helper functions and the final method to be called when a user reads an article. 
"""
# Importing the necessary libraries
from google.cloud import language_v1
from google_senti_analysis import analyze_entity_sentiment

# Defining global variables
# Media Bias ratings taken from AllSides
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

# # List of more highly recommended media sources based on a user's locale (Since all of the sources are non-Asian, no specific sources are recommended for the asian region.)
# LOCALE_BASED_RECS = {
#     'america': ['bbc', 'guardian', 'reuters'],
#     'europe': ['ap', 'cnbc', 'cnn', 'fox', 'new_york_post', 'newsweek', 'pbs', 'washington_examiner'],
# }

"""
When a reader reads an article, their respective entity-sentiment scores will be updated. (Only entities of type PERSON, LOCATION, ORG and EVENT will be tracked)

Parameters:
    - user_background: Dictionary with entities as keys and their corresponding sentiment as values.
    - article_responses: Contains the various entities and their respective sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
"""
def update_opinion(user, article_responses):
    relevant_entities = ['PERSON', 'LOCATION', 'ORG', 'EVENT']
    user_opinion = user.get_opinion() # TODO: @MY

    for article_entity in article_responses.entities:
        article_entity_name = article_entity.name
        article_entity_type = language_v1.Entity.Type(article_entity.type_).name

        if (article_entity_type in relevant_entities):
            curr_entity_key = (article_entity_name, article_entity_type)

            if (curr_entity_key in user_opinion): # If (entity_name, entity_type) exists
                curr_sentiment = user_opinion[curr_entity_key][0]
                num_of_read_articles = user_opinion[curr_entity_key][1]

                new_sentiment = ((curr_sentiment * num_of_read_articles) + (article_entity.salience * article_entity.sentiment.score)) / float(num_of_read_articles + 1)

                user_opinion[curr_entity_key][0] = new_sentiment
                user_opinion[curr_entity_key][1] = num_of_read_articles + 1

            else: # If (entity_name, entity_type) is new
                user_opinion[curr_entity_key][0] = (article_entity.salience * article_entity.sentiment.score)
                user_opinion[curr_entity_key][1] = 1

            

"""
When a reader reads an article, their political bias scores will be updated. Returns the new political bias score for the given user.

Parameters:
    - user_political_bias: The user's current political bias, measured based on the user's initial declaration (if any) and the accumulatation of all the articles read by the user. It is the form of (baseline_bias, bias_based_on_articles_read, num_of_articles_read). baseline_bias is the number assgined based on the user's declaration, bias_based_on_articles_read is the average bias of all the articles read and num_of_articles_read refers to the number of articles read by the reader thus far.
    - curr_source_bias: The media bias rating (Taken from AllSides)
"""
def update_political_bias(user, curr_source_bias):
    user_political_bias = user.get_political_bias() # TODO: @MY
    baseline_bias = user_political_bias[0]
    bias_based_on_articles_read = user_political_bias[1]
    num_of_articles_read = user_political_bias[2]

    new_bias_based_on_articles_read = ((bias_based_on_articles_read * num_of_articles_read) + curr_source_bias) / float(num_of_articles_read + 1)

    return (baseline_bias, new_bias_based_on_articles_read, num_of_articles_read + 1)

"""
FINAL FUNCTION THAT NEEDS TO BE CALLED.

Updates a user's opinions and political bias based on the article that they are currently reading.

Parameters:
    - user: The user object stored in the backend
    - article: The article object containing at least the body text and source information
"""
def read_article(user, article):
    # Update the user's opinions
    body_text = article.get_body_text() # TODO: @MY
    article_response = analyze_entity_sentiment(body_text)
    update_opinion(user, article_response)

    # Update the user's political bias
    article_source = article.get_source() # TODO: @MY
    source_bias = MEDIA_BIAS_RATINGS[article_source]
    update_political_bias(user, source_bias)