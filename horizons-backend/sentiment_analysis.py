# Imports the Google Cloud client library
import math
import nltk
import spacy
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy import displacy
from collections import Counter
import en_core_web_sm

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
Calculates how the possibly recommended article is going to differ from the article being currently read by the user. Does so by first extracting common entities from both articles. Then, the salience * sentiment score is calculated for each entity and accumulated for each article. Lastly, the overall difference is calculated, with a greater value suggesting a greater difference in sentiment.

Parameters:
    reading_article_response: Contains the various entities and their respective salience and sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
    rec_article_response: Contains the various entities and their respective salience and sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
"""
def diff_in_sentiment(reading_article_response, rec_article_response):
    reading_article_score = 0
    rec_article_score = 0

    for reading_article_entity in reading_article_response.entities:
        reading_article_entity_name = reading_article_entity.name
        reading_article_entity_type = language_v1.Entity.Type(reading_article_entity.type_).name

        for rec_article_entity in rec_article_response.entities:
            rec_article_entity_name = rec_article_entity.name
            rec_article_entity_type = language_v1.Entity.Type(rec_article_entity.type_).name

            if (reading_article_entity_name == rec_article_entity_name and reading_article_entity_type == rec_article_entity_type):
                reading_article_score += (reading_article_entity.salience * reading_article_entity.sentiment.score)
                rec_article_score += (rec_article_entity.salience * rec_article_entity.sentiment.score)
                break

    diff_in_sentiment = rec_article_score - reading_article_score
    percent_diff = abs(diff_in_sentiment)/reading_article_score

    print('Sentiment score of the currently reading article: ' + str(reading_article_score))
    print('Sentiment score of the possibly recommended article: ' + str(rec_article_score))
    print('Overall change in sentiment: ' + str(diff_in_sentiment))
    print('Degree of change: ' + str((percent_diff)))

    return diff_in_sentiment, percent_diff

"""
Computes how much a user's current sentiments on various entities would change after reading a given article. 

Parameters:
    user_background: Dictionary with entities as keys and their corresponding sentiment as values.
    article_responses: Contains the various entities and their respective sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
"""
def overall_diff_in_opinion(user_background, article_responses):
    relevant_entities = ['PERSON', 'LOCATION', 'ORG', 'EVENT']
    accumulated_degree_of_change = 0
    for article_entity in article_responses.entities:
        article_entity_type = language_v1.Entity.Type(article_entity.type_).name
        if (article_entity_type in relevant_entities and article_entity in user_background[article_entity]):
            num_of_read_articles = user_background[article_entity][1]
            curr_sentiment = user_background[article_entity][0]

            new_sentiment = ((curr_sentiment * num_of_read_articles) + (article_entity.salience * article_entity.sentiment.score)) / float(num_of_read_articles + 1)
            accumulated_degree_of_change += abs(new_sentiment - curr_sentiment)
        else:
            accumulated_degree_of_change += abs(article_entity.salience * article_entity.sentiment.score)
    
    print('The overall change in opinion would be: ' + str(accumulated_degree_of_change))
    return accumulated_degree_of_change

"""
Measures how much a source's political bias differs from the user's.

Parameters:
    user_political_bias: The user's current political bias, measured based on the user's initial declaration (if any) and the accumulatation of all the articles read by the user. In the form of (baseline_bias, change, num_of_articles_read)
    curr_source_bias: The media bias rating (Taken from AllSides)
"""
# TODO: Need to figure what percentage of a reader's mind can be swayed? (Currently setting to 30%)
def diff_in_political_bias(user_political_bias, curr_source):
    curr_source_bias = MEDIA_BIAS_RATINGS[curr_source]

    baseline_bias = user_political_bias[0]
    curr_change = user_political_bias[1]
    curr_user_bias = (baseline_bias * 0.7) + (curr_change * 0.3)

    return curr_source_bias - curr_user_bias

"""
Measures if the media source has a different locale compared to the user. Articles written by a source of a different locale are more highly recommended so as to broaden the user's horizons.

Parameters:
    user_locale: The user's current locale collected during their initial declaration
    curr_source: The media source name
"""
# TODO: To complete
def diff_in_locale(user_locale, curr_source):
    recommended_sources = LOCALE_BASED_RECS[user_locale]

    if (curr_source in recommended_sources):
        return 1
    
    return 1

"""
Computes the recommendation score for a given article, with respect to the article being currently read by the user, as well the user's current opinions.

Parameters:
    diff_in_sentiment_score: Measures how different a given article is from the article being currently read. 
    diff_in_opinion_score: Measures how the user's opinion might differ after reading a given article. 
    diff_in_political_bias_score: Measures how the user's political bias differs from the source's bias.
    diff_in_locale: Measures how the user's locale is different from the source's locale.
    weights: A tuple of floats that are to be assigned as weights to each of the above scores. 
"""
# TODO: To complete
def recommendation_score(diff_in_sentiment_score, diff_in_opinion_score, diff_in_political_bias_score, diff_in_locale, weights):
    final_score = (diff_in_sentiment_score * weights[0]) + (diff_in_opinion_score * weights[1]) + (diff_in_political_bias_score * weights[2]) + (diff_in_locale * weights[3])

    print('The final recommendation score: ' + str(final_score))
    return final_score

"""
Selects the top 3 recommeded articles based on their recommendation scores. 

Parameters:
    article_arr: Array containing tuples of (article, timstamp_of_release, recommendation_score, diff_in_opinion_score) for the top 3 shortlisted articles.
"""
def shortlist_top_3(article_arr):
    article_arr.sort(key= lambda x: x[2], reversed=True)

    if (len(article_arr) < 3):
        return article_arr
    else:
        return article_arr[0:2]

"""
Ranks shortlisted articles. The article that seems to greatly differ from a user's current sentiments will be placed second. Between the other 2 articles, the one with the higher recommendation score will be ranked first. 

Parameters:
    article_arr: Array containing tuples of (article, timstamp_of_release, recommendation_score, diff_in_opinion_score) for the top 3 shortlisted articles.
"""
def ranking_articles(article_arr):
    ARTICLE_INDEX = 0
    TIMESTAMP_INDEX = 1
    REC_INDEX = 2
    DIFF_IN_OPINION_INDEX = 3

    if (len(article_arr) == 0): # If there are no articles to recommend at the moment
        return []
    
    # Step 1: Ranking the article that is most diff from the user's current sentiment as the second article
    ranked_articles = []

    second_article_index = -1
    highest_diff_in_opinion = 0

    for i in range(0, len(article_arr)):
        if (second_article == -1 or (article_arr[i][DIFF_IN_OPINION_INDEX] > highest_diff_in_opinion)):
            second_article = i
            highest_diff_in_opinion = article_arr[i][DIFF_IN_OPINION_INDEX]

    ranked_articles.append(article_arr.pop(second_article_index))

    # Step 2: If there are still at least 2 articles and the diff in sentiments is low, timestamp is also considered as a factor
    # TODO: Assuming that recommendation score is within 1. Need to check if this is the case
    if (len(article_arr) > 1 and 
        (abs(article_arr[0][REC_INDEX] >= 0.5)) and 
        ((abs(article_arr[1][REC_INDEX] >= 0.5)) and 
         (abs(article_arr[0][REC_INDEX] - article_arr[1][REC_INDEX]) < 0.25))):
        
        if (article_arr[0][TIMESTAMP_INDEX] > article_arr[1][TIMESTAMP_INDEX]):
            ranked_articles.append(article_arr.pop(0))
            ranked_articles.append(article_arr.pop(0))
        else:
            ranked_articles.append(article_arr.pop(1))
            ranked_articles.append(article_arr.pop(0))

        return ranked_articles

    # Step 3: If there is only 1 article or if diff in recommendation scores are drastically diff between the 2 articles, just rank by the recommendation scores
    first_article_index = -1
    highest_rec_score = 0

    for i in range(0, len(article_arr)):
        if (first_article_index == -1 or (article_arr[i][1] > highest_rec_score)):
            first_article_index = i
            highest_rec_score = article_arr[i][1]

    ranked_articles.append(article_arr.pop(first_article_index))
    ranked_articles.append(article_arr.pop(0))

    return ranked_articles
    
# Testing
reading_text = analyze_entity_sentiment("Ice cream is good.")
rec_text = analyze_entity_sentiment("Ice cream is bad.")
diff_in_sentiment(reading_text, rec_text)