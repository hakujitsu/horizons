from enum import Enum
from scrapers.cnn_scraper import parseArticle as parseCNN
from scrapers.guardian_scraper import parseArticle as parseGuardian



# class syntax
class NewsSource(Enum):
    AP_NEWS = 1
    BBC = 2
    CNBC = 3
    CNN = 4
    FOX = 5
    GUARDIAN = 6
    NYP = 7
    NEWSWEEK = 8
    PBS = 9
    REUTERS = 10
    WASHINGTON = 11

def getArticleSource(url):
    if ("apnews.com" in url):
        return NewsSource.AP_NEWS
    elif ("bbc.com" in url):
        return NewsSource.BBC
    elif ("cnbc.com" in url):
        return NewsSource.CNBC
    elif ("edition.cnn.com" in url):
        return NewsSource.CNN
    elif ("foxnews.com" in url):
        return NewsSource.FOX
    elif ("theguardian.com" in url):
        return NewsSource.GUARDIAN
    elif ("nypost.com" in url):
        return NewsSource.NYP
    elif ("newsweek.com" in url):
        return NewsSource.NEWSWEEK
    elif ("pbs.org" in url):
        return NewsSource.PBS
    elif ("reuters.com" in url):
        return NewsSource.REUTERS
    elif ("washingtonexaminer.com" in url):
        return NewsSource.WASHINGTON
    return None

def scrapeArticle(url):
    source = getArticleSource(url)
    if (source == None):
        return None, None

    if (source == NewsSource.CNN):
        return parseCNN(url)
    elif (source == NewsSource.GUARDIAN):
        return parseGuardian(url)
    return None, None