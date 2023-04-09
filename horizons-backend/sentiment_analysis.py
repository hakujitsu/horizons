"""
This file contains the functions required to carry out sentiment analysis on a given article.
"""
from utils.scraper_utils import NewsSource
from google.cloud import language_v1 # Imports the Google Cloud client library
from google_senti_analysis import analyze_entity_sentiment

# Based on AllSides Media Bias ratings
MEDIA_BIAS_RATINGS = {
    NewsSource.AP_NEWS.value: -1.5,
    NewsSource.BBC.value: -0.8,
    NewsSource.CNBC.value: -0.9,
    NewsSource.CNN.value: -3.8,
    NewsSource.FOX.value: 4,
    NewsSource.GUARDIAN.value: -2.4,
    NewsSource.NYP.value: 1.8,
    NewsSource.NEWSWEEK.value: 0.5,
    NewsSource.PBS.value: -1.1,
    NewsSource.REUTERS.value: 0,
    NewsSource.WASHINGTON.value: 2.3,
}

# Since all of the sources are non-Asian, no specific sources are recommended for the asian region.
LOCALE_BASED_RECS = {
    'USA': [NewsSource.BBC.value, NewsSource.GUARDIAN.value, NewsSource.REUTERS.value],
    'UK': [NewsSource.AP_NEWS.value, NewsSource.CNBC.value, NewsSource.CNN.value, NewsSource.FOX.value,
               NewsSource.NYP.value, NewsSource.NEWSWEEK.value, NewsSource.PBS.value, NewsSource.WASHINGTON.value],
}

"""
Calculates how the possibly recommended article is going to differ from the article being currently read by the user. Does so by first extracting common entities from both articles. Then, the salience * sentiment score is calculated for each entity and accumulated for each article. Lastly, the overall difference is calculated, with a greater value suggesting a greater difference in sentiment.

Parameters:
    - reading_article_response: Contains the various entities and their respective salience and sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
    - rec_article_response: Contains the various entities and their respective salience and sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
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
                # print('----')
                # print(reading_article_score)
                # print(rec_article_score)
                # print('----')
                # break

    print(rec_article_score)
    print(reading_article_score)
    diff_in_sentiment = abs(rec_article_score - reading_article_score)

    return diff_in_sentiment # TODO: Have to normalise across all shortlisted articles

"""
Computes how much a user's current sentiments on various entities would change after reading a given article. 

Parameters:
    - user_opinion: Dictionary with (entity_name, entity_type) as keys and their (sentiment, number of articles read) as values.
    - article_responses: Contains the various entities and their respective sentiment scores. It is the output from analysing the article using analyze_entity_sentiment
"""
def overall_diff_in_opinion(user_opinion, article_responses):
    relevant_entities = ['PERSON', 'LOCATION', 'ORG', 'EVENT']
    accumulated_degree_of_change = 0

    for article_entity in article_responses.entities:
        article_entity_name = article_entity.name
        article_entity_type = language_v1.Entity.Type(article_entity.type_).name
        curr_entity_key = (article_entity_name, article_entity_type)

        if (article_entity_type in relevant_entities and curr_entity_key in user_opinion):
            curr_sentiment = user_opinion[curr_entity_key][0]
            num_of_read_articles = user_opinion[curr_entity_key][1]

            new_sentiment = ((curr_sentiment * num_of_read_articles) + (article_entity.salience * article_entity.sentiment.score)) / float(num_of_read_articles + 1)
            accumulated_degree_of_change += abs(new_sentiment - curr_sentiment)

        else:
            accumulated_degree_of_change += abs(article_entity.salience * article_entity.sentiment.score)

    return accumulated_degree_of_change # TODO: Have to normalise across all shortlisted articles

"""
Measures how much a source's political bias differs from the user's and returns this value.

Parameters:
    - user_political_bias: The user's current political bias, measured based on the user's initial declaration (if any) and the accumulatation of all the articles read by the user. In the form of (baseline_bias, change, num_of_articles_read)
    - curr_source_bias: The media bias rating (Taken from AllSides)
"""
# TODO: Need to figure what percentage of a reader's mind can be swayed? (Currently setting to 30%)
def diff_in_political_bias(user_political_bias, curr_source):
    curr_source_bias = MEDIA_BIAS_RATINGS[curr_source] # TODO: Must make sure the curr_source is of the right format

    baseline_bias = user_political_bias[0]
    avg_bias_of_read_articles = user_political_bias[1]
    curr_user_bias = (baseline_bias * 0.7) + (avg_bias_of_read_articles * 0.3)

    return abs(curr_source_bias - curr_user_bias) # The negative/positive is important! 

def diff_in_political_bias_articles(read_source, curr_source):
    curr_source_bias = MEDIA_BIAS_RATINGS[curr_source] # TODO: Must make sure the curr_source is of the right format
    read_source_bias = MEDIA_BIAS_RATINGS[read_source]

    return abs(curr_source_bias - read_source_bias) # The negative/positive is important! 

"""
Measures if the media source has a different locale compared to the user. Articles written by a source of a different locale are more highly recommended so as to broaden the user's horizons.

Parameters:
    - user_locale: The user's current locale collected during their initial declaration
    - curr_source: The media source name
"""
def diff_in_locale(user_locale, curr_source):
    recommended_sources = LOCALE_BASED_RECS[user_locale]

    if (curr_source in recommended_sources):
        return 1 # Returns an arbitrary value (not a very high score as this is not a very significant factor)
    return 0.5 # TODO: check if this is an appropriate factor