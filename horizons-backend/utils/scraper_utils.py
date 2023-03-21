from enum import Enum
from scrapers.ap_scraper import parseArticle as parseAP
from scrapers.bbc_scraper import parseArticle as parseBBC
from scrapers.cnbc_scraper import parseArticle as parseCNBC
from scrapers.cnn_scraper import parseArticle as parseCNN
from scrapers.fox_scraper import parseArticle as parseFox
from scrapers.guardian_scraper import parseArticle as parseGuardian
from scrapers.new_york_post_scraper import parseArticle as parseNYP
from scrapers.newsweek_scraper import parseArticle as parseNewsweek
from scrapers.pbs_scraper import parseArticle as parsePBS
from scrapers.reuters_scraper import parseArticle as parseReuters
from scrapers.washington_examiner_scraper import parseArticle as parseWE

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
        return None, None, None

    if (source == NewsSource.AP_NEWS):
        header, article = parseAP(url)
        return source, header, article
    elif (source == NewsSource.BBC):
        header, article = parseBBC(url)
        return source, header, article
    elif (source == NewsSource.CNBC):
        header, article = parseCNBC(url)
        return source, header, article
    elif (source == NewsSource.CNN):
        header, article = parseCNN(url)
        return source, header, article
    elif (source == NewsSource.FOX):
        header, article = parseFox(url)
        return source, header, article
    elif (source == NewsSource.NYP):
        header, article = parseNYP(url)
        return source, header, article
    elif (source == NewsSource.NEWSWEEK):
        header, article = parseNewsweek(url)
        return source, header, article
    elif (source == NewsSource.PBS):
        header, article = parsePBS(url)
        return source, header, article
    elif (source == NewsSource.REUTERS):
        header, article = parseReuters(url)
        return source, header, article
    elif (source == NewsSource.WASHINGTON):
        header, article = parseWE(url)
        return source, header, article
    return None, None, None