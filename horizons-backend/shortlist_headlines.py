"""
This files contains functions to shortlist possible recommendations purely based on their headlines, before further analysing the body text of the articles. 
"""
# Import necessary libraries
import en_core_web_sm
import string
from google.cloud import language_v1 # Imports the Google Cloud client library
from google_senti_analysis import analyze_entity_sentiment
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentiment_analysis import diff_in_sentiment
from spacy import displacy

"""
Computing the similarity between headlines by extracting the common named entities between the 2 headlines and returns how significant they are in the recommended article's headline to gauge if it is likely to be a relevant article.

Parameters:
    - read_headline: Headline of the article that the user is currently reading
    - rec_headline: Headline of the article that is to be possibly recommended

Note: Spacy is case sensitive for named entity recognition
"""
def ner_similarity_percent(read_headline, rec_headline):
    tokenized_read_headline = {}
    tokenized_rec_headline = {}

    # Step 1: Remove any stopwords and punctuations from the headlines
    stop_words = set(stopwords.words('english')) # Case doesn't matter
    puncutations = string.punctuation

    read_headline = word_tokenize(read_headline)
    read_headline_len = len(read_headline)
    read_headline = [w for w in read_headline if (w not in stop_words and w not in puncutations)]
    for term in read_headline:
        if (term in tokenized_read_headline):
            tokenized_read_headline[term] += 1
        else:
            tokenized_read_headline[term] = 1

    rec_headline = word_tokenize(rec_headline)
    rec_headline_len = len(rec_headline)
    rec_headline = [w for w in rec_headline if (w not in stop_words and w not in puncutations)]
    for term in rec_headline:
        if (term in tokenized_rec_headline):
            tokenized_rec_headline[term] += 1
        else:
            tokenized_rec_headline[term] = 1

    # Step 2: Extracting common terms found between both headlines
    common_terms = []
    for read_headline_term in tokenized_read_headline:
        for rec_headline_term in tokenized_rec_headline:
            # Usually the named entities have their first letter as a capital letter
            if (not read_headline_term[0].islower() and not rec_headline_term[0].islower() and read_headline_term.lower() ==  rec_headline_term.lower()):
                if ((read_headline_term, rec_headline_term) not in common_terms):
                    common_terms.append((read_headline_term, rec_headline_term)) # Ensure that unique pairs are added

    # Step 3: Only retain pairs that at least have one term being recognised as a named entity (This is to allow for cases where the case of the terms and other negligible factors affects its recognition as a named entity)
    named_entities_rec_headline = []
    nlp = en_core_web_sm.load()
    non_valid_ner_cats = ['PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL']

    for paired_terms in common_terms:
        entity_of_first_term = nlp(paired_terms[0]).ents
        entity_of_sec_term = nlp(paired_terms[1]).ents

        if len(entity_of_first_term) > 0 and entity_of_first_term[0].label_ not in non_valid_ner_cats:
            named_entities_rec_headline.append(paired_terms[1])
        elif len(entity_of_sec_term) > 0 and entity_of_sec_term[0].label_ not in non_valid_ner_cats:
            named_entities_rec_headline.append(paired_terms[1])

    # Step 4: Calculating the percentage of similarity in terms of named entities between the 2 headlines
    num_of_significant_terms = 0
    for term in named_entities_rec_headline:
        num_of_significant_terms += tokenized_rec_headline[term]

    percent_of_significance = float(num_of_significant_terms)/float(rec_headline_len)

    return percent_of_significance

"""
Computing the similarity between headlines by unigrams and returns the percentage of overlap in terms of unigrams.

Parameters:
    - read_headline: Headline of the article that the user is currently reading
    - rec_headline: Headline of the article that is to be possibly recommended
"""
def unigram_similarity(read_headline, rec_headline):
    read_headline_unigrams = {}
    rec_headline_unigrams = {}

    read_headline = read_headline.lower()
    read_headline_len = len(read_headline)
    for i in range(0, len(read_headline)):
        if (read_headline[i] in read_headline_unigrams):
            read_headline_unigrams[read_headline[i]] += 1
        else:
            read_headline_unigrams[read_headline[i]] = 1

    rec_headline = rec_headline.lower()
    rec_headline_len = len(rec_headline)
    for i in range(0, len(rec_headline)):
        if (rec_headline[i] in rec_headline_unigrams):
            rec_headline_unigrams[rec_headline[i]] += 1
        else:
            rec_headline_unigrams[rec_headline[i]] = 1

    num_of_overlapping_unigrams = 0

    for unigram in list(read_headline_unigrams.keys()) :
        if (unigram in rec_headline):
            num_of_overlapping_unigrams += read_headline_unigrams[unigram] + rec_headline_unigrams[unigram]

    percentage_similarity = float(num_of_overlapping_unigrams)/float(read_headline_len + rec_headline_len)
    return percentage_similarity

"""
Computing the similarity between headlines by unigrams and returns the percentage of overlap in terms of bigrams.

Parameters:
    - read_headline: Headline of the article that the user is currently reading
    - rec_headline: Headline of the article that is to be possibly recommended
"""
def bigram_similarity(read_headline, rec_headline):
    read_headline_bigrams = {}
    rec_headline_bigrams = {}

    read_headline = read_headline.lower()
    read_headline = '<s> ' + read_headline
    read_headline += ' <\s>'
    read_headline_len = len(read_headline)
    for i in range(0, len(read_headline) - 1):
        if (read_headline[i:i+2] in read_headline_bigrams):
            read_headline_bigrams[read_headline[i:i+2]] += 1
        else:
            read_headline_bigrams[read_headline[i:i+2]] = 1
    
    rec_headline = rec_headline.lower()
    rec_headline = '<s> ' + rec_headline
    rec_headline += ' <\s>'
    rec_headline_len = len(rec_headline)
    for i in range(0, len(rec_headline) - 1):
        if (rec_headline[i:i+2] in rec_headline_bigrams):
            rec_headline_bigrams[rec_headline[i:i+2]] += 1
        else:
            rec_headline_bigrams[rec_headline[i:i+2]] = 1

    num_of_overlapping_bigrams = 0

    for bigram in list(read_headline_bigrams.keys()):
        if (bigram in rec_headline):
            num_of_overlapping_bigrams += read_headline_bigrams[bigram] + rec_headline_bigrams[bigram]
    
    percentage_similarity = float(num_of_overlapping_bigrams)/float(read_headline_len + rec_headline_len)
    return percentage_similarity

"""
FINAL FUNCTION THAT NEEDS TO BE CALLED.

Calculates the degree of similarity between the headline of a currently being read headline and that of a possible recommendation to gauge the relevance of the recommended article.

Parameters:
    - read_headline: Headline of the article that the user is currently reading
    - rec_headline: Headline of the article that is to be possibly recommended
"""
# TODO: Need to choose between methods 1 and 2 if we are doing this
def headline_similarity_score(read_headline, rec_headline):
    # Method 1: Using spacy, unigrams and bigrams (To later compare if this is faster compared to using Google Cloud nlp)
    final_score = (ner_similarity_percent(read_headline, rec_headline) * 0.7) + (unigram_similarity(read_headline, rec_headline) * 0.15) + (bigram_similarity(read_headline, rec_headline) * 0.15) 

    # Method 2: Using google cloud sentiment analysis
    read_headline_response = analyze_entity_sentiment(read_headline)
    rec_headline_response = analyze_entity_sentiment(rec_headline)
    final_score = diff_in_sentiment(read_headline_response, rec_headline_response)

    return final_score # TODO @MY if score is > 0.5 we can shortlist articles?