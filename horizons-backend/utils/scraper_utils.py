from enum import Enum
import requests
from utils.constant_utils import REQUEST_HEADER
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
    AP_NEWS = "AP News"
    BBC = "BBC"
    CNBC = "CNBC"
    CNN = "CNN"
    FOX = "Fox News"
    GUARDIAN = "The Guardian"
    NYP = "New York Post"
    NEWSWEEK = "Newsweek"
    PBS = "PBS NewsHour"
    REUTERS = "Reuters"
    WASHINGTON = "Washington Examiner"

def getArticleSource(url):
    if ("apnews.com" in url):
        return NewsSource.AP_NEWS
    elif ("bbc.com" in url):
        return NewsSource.BBC
    elif ("cnbc.com" in url):
        return NewsSource.CNBC
    elif ("cnn.com" in url):
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

def getArticleHtml(url):
    return requests.get(url,headers=REQUEST_HEADER)

def scrapeArticleWithUrl(url):
    source = getArticleSource(url)
    if (source == None):
        return None, None, None
    html = getArticleHtml(url).content
    return scrapeArticleWithHtml(url, html)

def scrapeArticleWithHtml(url, html):
    source = getArticleSource(url)
    if (source == None):
        return None, None, None

    if (source == NewsSource.AP_NEWS):
        header, article = parseAP(html)
        return source, header, article
    elif (source == NewsSource.BBC):
        header, article = parseBBC(html)
        return source, header, article
    elif (source == NewsSource.CNBC):
        header, article = parseCNBC(html)
        return source, header, article
    elif (source == NewsSource.CNN):
        header, article = parseCNN(html)
        return source, header, article
    elif (source == NewsSource.FOX):
        header, article = parseFox(html)
        return source, header, article
    elif (source == NewsSource.GUARDIAN):
        header, article = parseGuardian(html)
        return source, header, article
    elif (source == NewsSource.NYP):
        header, article = parseNYP(html)
        return source, header, article
    elif (source == NewsSource.NEWSWEEK):
        header, article = parseNewsweek(html)
        return source, header, article
    elif (source == NewsSource.PBS):
        header, article = parsePBS(html)
        return source, header, article
    elif (source == NewsSource.REUTERS):
        header, article = parseReuters(html)
        return source, header, article
    elif (source == NewsSource.WASHINGTON):
        header, article = parseWE(html)
        return source, header, article
    return None, None, None