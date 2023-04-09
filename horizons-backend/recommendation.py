"""
This file contains the functions required to shortlist and rank the recommended articles.
"""

# Import the necessary libraries/functions
from google_senti_analysis import analyze_entity_sentiment
from sentiment_analysis import diff_in_sentiment, overall_diff_in_opinion, diff_in_political_bias, diff_in_locale, diff_in_political_bias_articles
from shortlist_headlines import headline_similarity_score
import multiprocessing
from typing import List, Tuple


WEIGHTS = [1, 1, 1, 1] # TODO: Need to figure out the best weights

"""
Computes the recommendation score for a given article, with respect to the article being currently read by the user, as well the user's current opinions. This score is then returned.

Parameters:
    - diff_in_sentiment_score: Measures how different a given article is from the article being currently read. 
    - diff_in_opinion_score: Measures how the user's opinion might differ after reading a given article. 
    - diff_in_political_bias_score: Measures how the user's political bias differs from the source's bias.
    - diff_in_locale: Measures how the user's locale is different from the source's locale.
    - weights: A tuple of floats that are to be assigned as weights to each of the above scores. Tuple will be in the format of (sentiment_diff_weight, opinion_diff_weight, political_bias_weight, locale_diff_weight)
"""
def recommendation_score(diff_in_sentiment_score, diff_in_opinion_score, diff_in_political_bias_score, diff_in_locale, weights):
    print(weights)

    f_1 = (diff_in_sentiment_score * weights[0])
    f_2 = (diff_in_opinion_score * weights[1])
    f_3 = (diff_in_political_bias_score * weights[2])
    f_4 = (diff_in_locale * weights[3])

    print('sentiment score: ' + str(f_1))
    print('opinion score: ' + str(f_2))
    print('political bias score: ' + str(f_3))
    print('locale score: ' + str(f_4) + '\n')
    return f_1 + f_2 + f_3 + f_4

"""
Selects the top 3 recommeded articles based on their recommendation scores. 

Returns the top 3 articles to be ranked.

Parameters:
    - article_arr: Array containing tuples of (article, timstamp_of_release, recommendation_score, diff_in_opinion_score) for the top 3 shortlisted articles.
"""
def shortlist_top_3(article_arr):
    # article_arr.sort(key= lambda x: x[2], reverse=True)

    # if (len(article_arr) < 3):
    #     return article_arr
    # else:
    #     return article_arr[0:3]
    DIFF_IN_ARTICLES_INDEX = 2
    DIFF_BET_USER_AND_ARTICLE_INDEX = 3

    article_arr.sort(key= lambda x: x[DIFF_IN_ARTICLES_INDEX], reverse=True) # Sort by sentiment first

    if (len(article_arr) > 6):
        half = (len(article_arr) // 2) + 1 # Round up
        article_arr = article_arr[:half]

        final_list = []
        article_arr.sort(key= lambda x: x[DIFF_BET_USER_AND_ARTICLE_INDEX], reverse=True) # Sort by opinions first
        # Extracting the top 2 articles most diff in opinion and 1 that is least diff in opinion
        final_list.append(article_arr[0])
        final_list.append(article_arr[1])
        final_list.append(article_arr[-1])

        return final_list
    else:
        return article_arr



"""
Ranks shortlisted articles. The article that seems to greatly differ from a user's current sentiments will be placed second. Between the other 2 articles, the one with the higher recommendation score will be ranked first. 

Returns the ranked, top 3 articles to recommend to the user. 

Parameters:
    - article_arr: Array containing tuples of (article, timstamp_of_release, recommendation_score, diff_in_opinion_score) for the top 3 shortlisted articles.
"""
def ranking_articles(article_arr):
    ARTICLE_INDEX = 0
    TIMESTAMP_INDEX = 1
    REC_INDEX = 2
    DIFF_IN_OPINION_INDEX = 3

    if (len(article_arr) <= 1): # If there are no articles / only one article to recommend at the moment
        return article_arr

    # Step 1: Ranking the article that is most diff from the user's current sentiment as the second article
    ranked_articles = []

    second_article_index = -1
    highest_diff_in_opinion = 0

    for i in range(0, len(article_arr)):
        if (second_article_index == -1 or (article_arr[i][DIFF_IN_OPINION_INDEX] > highest_diff_in_opinion)):
            second_article_index = i
            highest_diff_in_opinion = article_arr[i][DIFF_IN_OPINION_INDEX]

    ranked_articles.append(article_arr.pop(second_article_index))

    # Step 2: If there are still at least 2 articles and the diff in the recommendation scores between them is relatively low, timestamp is also considered as a factor
    # rec_lean_towards_first_article = article_arr[0][REC_INDEX] / article_arr[0][REC_INDEX] + article_arr[1][REC_INDEX]

    # if (len(article_arr) > 1 and rec_lean_towards_first_article >= 0.4 and rec_lean_towards_first_article <= 0.6):
    #     if (article_arr[0][TIMESTAMP_INDEX] > article_arr[1][TIMESTAMP_INDEX]):
    #         ranked_articles.append(article_arr.pop(0))
    #         ranked_articles.append(article_arr.pop(0))
    #     else:
    #         ranked_articles.append(article_arr.pop(1))
    #         ranked_articles.append(article_arr.pop(0))

    #     return ranked_articles

    # Step 3: If there is only 1 article or if diff in recommendation scores are drastically diff between the 2 articles, just rank by the recommendation scores
    first_article_index = -1
    highest_rec_score = 0

    for i in range(0, len(article_arr)):
        if (first_article_index == -1 or (article_arr[i][REC_INDEX] > highest_rec_score)):
            first_article_index = i
            highest_rec_score = article_arr[i][REC_INDEX]

    ranked_articles.insert(0, article_arr.pop(first_article_index))
    if (len(article_arr) > 0): 
        ranked_articles.append(article_arr.pop(0))

    return ranked_articles

def calculate_rec_article_scores(rec_article: Tuple, shared_data: dict) -> Tuple[dict, dict, float, str]:
    read_article_response = shared_data['read_article_response']
    user_opinion = shared_data['user_opinion']
    user_political_bias = shared_data['user_political_bias']
    user_locale = shared_data['user_locale']
    read_article_source = shared_data['read_article_source']
    # calculate acc_score and prec_score for the article
    rec_article_source = rec_article[3] # TODO @MY need this method
    rec_article_body_text = rec_article[2] # TODO @MY need this method
    timestamp = "" # TODO @MY need this method (if we want to scrape this)
    rec_article_response = analyze_entity_sentiment(rec_article_body_text)

    # Computing the diff scores
    sentiment_diff_score = diff_in_sentiment(read_article_response, rec_article_response)
    opinion_diff_score = overall_diff_in_opinion(user_opinion, rec_article_response)
    political_bias_diff_score = diff_in_political_bias(user_political_bias, rec_article_source)
    locale_diff_score = diff_in_locale(user_locale, rec_article_source)

    # Method 1: Based on shortlisted and ranked based on an recommendation score, where each factor is assigned equal weight
    # recommendation_score(sentiment_diff_score, opinion_diff_score, political_bias_diff_score, local_diff_score, [1, 1, 1, 1])

    # Method 2: Based on shortlisted and ranked based on an recommendation score, where each factor is assigned a different weight to ensure that it is sufficiently significant in the recommendation score
    # overall_rec_score = recommendation_score(sentiment_diff_score, opinion_diff_score, political_bias_diff_score, local_diff_score, [1000, 100, 1, 1])

    # rec_article_scores.append((rec_article, timestamp, overall_rec_score, opinion_diff_score))

    # Method 3: Articles are first shortlisted based on the difference between the articles, and then the difference between the readers's opinions and that of the article's.
    # rec_article_scores.append((rec_article, timestamp, (sentiment_diff_score * 1000) + local_diff_score, (opinion_diff_score) + political_bias_diff_score))

    # Method 4: Articles are first shortlisted based on the difference between the articles, and then the difference between the readers's opinions and that of the article's. This additionally includes the difference in the soures' political bias.(FINAL)
    diff_between_articles = (sentiment_diff_score * 1000) + diff_in_political_bias_articles(read_article_source, rec_article_source)
    diff_between_reader_and_rec_article = opinion_diff_score + political_bias_diff_score + locale_diff_score

    overall_rec_score = (rec_article[0], timestamp, diff_between_articles, diff_between_reader_and_rec_article)

    # overall_rec_score = recommendation_score(sentiment_diff_score, opinion_diff_score, political_bias_diff_score, locale_diff_score, WEIGHTS)

    return overall_rec_score

def calculate_scores_for_articles(articles, read_article_response, user_opinion, user_political_bias, user_locale, read_article_source):
    article_tuples = list()
    for idx, a in enumerate(articles):
        article_tuples.append((idx, a.title, a.article, a.source.value))

    with multiprocessing.Manager() as manager:
        shared_data = manager.dict()
        shared_data['read_article_response'] = read_article_response
        shared_data['user_opinion'] = user_opinion
        shared_data['user_political_bias'] = user_political_bias
        shared_data['user_locale'] = user_locale
        shared_data['read_article_source'] = read_article_source.value

        # Create a pool of worker processes
        with multiprocessing.Pool() as pool:
            # Call calculate_scores_for_articles for each article using pool.map()
            results = pool.starmap(calculate_rec_article_scores, [(article, shared_data) for article in article_tuples])

            print(results)
            return_value = list()
            for a in results:
                new_tuple = list(a)
                idx = a[0]
                new_tuple[0] = articles[idx]
                return_value.append(tuple(new_tuple))

            return return_value


"""
FINAL FUNCTION THAT NEEDS TO BE CALLED.

Calculates the degree of similarity between the headline of a currently being read headline and that of a possible recommendation to gauge the relevance of the recommended article.

Returns the list of top 3, ranked articles (In the same format as the possible_articles_arr)

Parameters:
    - read_headline: Headline of the article that the user is currently reading
    - rec_headline: Headline of the article that is to be possibly recommended
"""
def get_final_recommendations(user, read_article, possible_articles_arr):
    # User information
    user_opinion = user.get_opinion() # TODO @MY need this method
    user_political_bias = user.get_political_bias() # TODO @MY need this method
    user_locale = user.get_locale() # TODO @MY need this method

    # Information on the article being currently read
    read_article_source = read_article.source
    read_article_headline = read_article.title # TODO @MY need this method
    read_article_body_text = read_article.article # TODO @MY need this method
    read_article_response = read_article.getEntitySentiment()

    if (read_article_response == None):
        return []

    # If shortlisting by headlines first (to produce the final 10 to 15 articles)
    if (len(possible_articles_arr) > 15):
        rec_article_scores = []
        for rec_article in possible_articles_arr:
            rec_article_headline = rec_article.title # TODO @MY need this method
            rec_article_scores.append((rec_article, headline_similarity_score(read_article_headline, rec_article_headline)))

        rec_article_scores.sort(key= lambda x: x[1], reverse=True)
        possible_articles_arr = rec_article_scores[0:15]
        possible_articles_arr = list(map(lambda a: a[0], possible_articles_arr))

    # Main shortlisting
    rec_article_scores = calculate_scores_for_articles(possible_articles_arr, read_article_response, user_opinion, user_political_bias, user_locale, read_article_source)
    # print(rec_article_scores) # For testing
    top_3_rec_articles = shortlist_top_3(rec_article_scores)
    # print(top_3_rec_articles) # For testing

    articles_to_return = list(map(lambda a: a[0], ranking_articles(top_3_rec_articles)))

    # for article in articles_to_return: # For testing
    #     print(article.title)

    return articles_to_return
