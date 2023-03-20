# from bs4 import BeautifulSoup as soup, NavigableString
# import requests
from scraper_utils import scrapeArticle

def getSimilarArticles(url):
    title, article = scrapeArticle(url)
    if (title == None or article == None):
      return []
    print(title)
    print("+++++++")
    print(article)

getSimilarArticles("https://edition.cnn.com/2023/03/20/china/china-xi-putin-russia-visit-analysis-intl-hnk-mic/index.html")