import math
import nltk
import spacy
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy import displacy
from collections import Counter
import en_core_web_sm

'''
Computing the similarity between headlines by extracting the named entities within each headline and calculating the similarity between them. (spacy version)

Currently this only works for sentences that have recognisable named entities. Another work around this is to get articles released at a similar timing, and study the overlap in terms among them. 

Note: Spacy is case sensitive for named entity recognition
'''
def ner_similarity_score(first_headline, sec_headline):
    tokenized_headline_1 = {}
    tokenized_headline_2 = {}

    # Step 1: Remove any stopwords and punctuations from the headlines #TODO: Need to remove punctuation, may not be necessary depending on the scraping
    stop_words = set(stopwords.words('english')) # Case doesn't matter
    puncutations = string.punctuation

    first_headline = word_tokenize(first_headline)
    first_headline_len = len(first_headline)
    first_headline = [w for w in first_headline if (w not in stop_words and w not in puncutations)]
    for term in first_headline:
        if (term in tokenized_headline_1):
            tokenized_headline_1[term] += 1
        else:
            tokenized_headline_1[term] = 1

    sec_headline = word_tokenize(sec_headline)
    sec_headline_len = len(sec_headline)
    sec_headline = [w for w in sec_headline if (w not in stop_words and w not in puncutations)]
    for term in sec_headline:
        if (term in tokenized_headline_2):
            tokenized_headline_2[term] += 1
        else:
            tokenized_headline_2[term] = 1

    # Step 2: Extracting common terms found between both headlines
    common_terms = []
    for first_headline_term in tokenized_headline_1:
        for sec_headline_term in tokenized_headline_2:
            # Usually the named entities have their first letter as a capital letter
            if (not first_headline_term[0].islower() and not sec_headline_term[0].islower() and first_headline_term.lower() ==  sec_headline_term.lower()):
                if ((first_headline_term, sec_headline_term) not in common_terms):
                    common_terms.append((first_headline_term, sec_headline_term)) # Ensure that unique pairs are added

    # Step 3: Only retain pairs that at least have one term being recognised as a named entity (This is to allow for cases where the case
    # of the terms and other negligible factors affects its recognition as a named entity)
    named_entities_headline_1 = []
    named_entities_headline_2 = []
    nlp = en_core_web_sm.load()
    non_valid_ner_cats = ['PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL']
    for paired_terms in common_terms:
        entity_of_first_term = nlp(paired_terms[0]).ents
        entity_of_sec_term = nlp(paired_terms[1]).ents
        if len(entity_of_first_term) > 0 and entity_of_first_term[0].label_ not in non_valid_ner_cats:
            named_entities_headline_1.append(paired_terms[0])
            named_entities_headline_2.append(paired_terms[1])
        elif len(entity_of_sec_term) > 0 and entity_of_sec_term[0].label_ not in non_valid_ner_cats:
            named_entities_headline_1.append(paired_terms[0])
            named_entities_headline_2.append(paired_terms[1])

    # Step 4: Calculating the percentage of similarity in terms of named entities between the 2 headlines 
    percent_of_significance = 100
    num_of_significant_terms = 0

    for term in named_entities_headline_1:
        num_of_significant_terms += tokenized_headline_1[term]
    
    percent_of_significance = min(percent_of_significance, float(num_of_significant_terms)/float(first_headline_len))
    num_of_significant_terms = 0 # Resetting

    for term in named_entities_headline_2:
        num_of_significant_terms += tokenized_headline_2[term]
    
    percent_of_significance = min(percent_of_significance, float(num_of_significant_terms)/float(sec_headline_len))

    print('Percentage based on named entities: ' + str(percent_of_significance))
    #return percent_of_significance #TODO: Is this sensible?

'''
Computing the similarity between headlines by unigrams and calculating percentage of overlap in terms of unigrams.
'''
def unigram_similarity(first_headline, sec_headline):
    first_headline_bigrams = {}
    sec_headline_bigrams = {}

    first_headline = first_headline.lower()
    first_headline_len = len(first_headline)
    for i in range(0, len(first_headline)):
        if (first_headline[i] in first_headline_bigrams):
            first_headline_bigrams[first_headline[i]] += 1
        else:
            first_headline_bigrams[first_headline[i]] = 1
    
    sec_headline = sec_headline.lower()
    sec_headline_len = len(sec_headline)
    for i in range(0, len(sec_headline)):
        if (sec_headline[i] in sec_headline_bigrams):
            sec_headline_bigrams[sec_headline[i]] += 1
        else:
            sec_headline_bigrams[sec_headline[i]] = 1

    num_of_overlapping_unigrams = 0

    for unigram in first_headline:
        if (unigram in sec_headline):
            num_of_overlapping_unigrams += first_headline[unigram] + sec_headline[unigram]
    
    percentage_similarity = float(num_of_overlapping_unigrams)/float(first_headline_len + sec_headline_len)
    print('Percentage similarity based on unigrams: ' + str(percentage_similarity))
    return percentage_similarity

'''
Computing the similarity between headlines by unigrams and calculating percentage of overlap in terms of bigrams.
'''
def bigram_similarity(first_headline, sec_headline):
    first_headline_bigrams = {}
    sec_headline_bigrams = {}

    first_headline = first_headline.lower()
    first_headline = '<s> ' + first_headline
    first_headline += ' <\s>'
    first_headline_len = len(first_headline)
    for i in range(0, len(first_headline) - 1):
        if (first_headline[i:i+2] in first_headline_bigrams):
            first_headline_bigrams[first_headline[i:i+2]] += 1
        else:
            first_headline_bigrams[first_headline[i:i+2]] = 1
    
    sec_headline = sec_headline.lower()
    sec_headline = '<s> ' + sec_headline
    sec_headline += ' <\s>'
    sec_headline_len = len(sec_headline)
    for i in range(0, len(sec_headline) - 1):
        if (sec_headline[i:i+2] in sec_headline_bigrams):
            sec_headline_bigrams[sec_headline[i:i+2]] += 1
        else:
            sec_headline_bigrams[sec_headline[i:i+2]] = 1

    num_of_overlapping_bigrams = 0

    for bigram in first_headline:
        if (bigram in sec_headline):
            num_of_overlapping_bigrams += first_headline[bigram] + sec_headline[bigram]
    
    percentage_similarity = float(num_of_overlapping_bigrams)/float(first_headline_len + sec_headline_len)
    print('Percentage similarity based on bigrams: ' + str(percentage_similarity))
    return percentage_similarity

def headline_similarity_score(first_headline, sec_headline):
    #TODO: Need to figure out the weights to be attached to each of the scoring systems above. Can consider the time of release of the articles as one of the scoring system.
    pass
'''
Calculating unexpectedness score.
'''
def unexpectedness_score():
    pass

'''
Calculating the cosine similarity score between 2 articles.
'''
def cosine_similarity(article_1, article_2):
    pass

'''
Calculating serendipity score. This unexpected * relevance. 
#TODO: Not sure if we need this. And if we are using version 2, we need to get the probabilities of consuming article 1, article 2 or both.
'''
def serendipity_score(prob_consuming_article_1, prob_consuming_article_2, prob_consuming_both_articles):
    # Version 1: TFIDF + Cosine similarity

    # Version 2
    score = - ((math.log2(prob_consuming_both_articles / (prob_consuming_article_1 * prob_consuming_article_2))) / math.log2(prob_consuming_both_articles))

    print(score)
    return score
    

if __name__ == "__main__":
    headlines = {
        'nytimes_mass_shooting': 'After mass shootings, Republicans expand access to guns',
        'nytimes_mexico_homicide': 'Mexico investigates migrant deaths in boarder city fire as homicide case',
        'wp_armed_grps': 'Armed groups on the right and left exploit the AR-15 as both tool and symbol',
        'wp_shooting_law': 'How a change in law could provide crucial seconds to survive a mass shooting'
    }
    headline_similarity_score(headlines['nytimes_mass_shooting'], headlines['wp_armed_grps']) #TODO: Maybe need some sort of lang model that can detect the connection between words like AR-15 and guns
    # sent = 'How a change in law could provide crucial seconds to survive a mass shooting'
    # nlp = en_core_web_sm.load()
    # print([(X.text, X.label_) for X in nlp(sent).ents])
