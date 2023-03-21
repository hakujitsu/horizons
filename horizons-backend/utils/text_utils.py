import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from string import punctuation
# nltk.download('stopwords')

punctuation = list(punctuation)
stop = set(stopwords.words('english'))

# Remove stopwards, ignore casing,
def buildQuery(title, article):
    text = (title + " " + article).lower()
    tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+")
    words1 = tokenizer.tokenize(text)
    tokens = [i for i in words1 if i not in stop]
    dict = sortFreqDict(wordListToFreqDict(tokens))
    mostFreqTokens = list(map(lambda x: x[1], dict[:10]))
    query = " ".join(mostFreqTokens)
    return query

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux