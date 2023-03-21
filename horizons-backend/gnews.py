import requests
import urllib.parse
from utils.scraper_utils import scrapeArticle
from utils.text_utils import buildQuery
from utils.constant_utils import BASE_URL, SUPPORTED_NEWS_SOURCES
import feedparser
import ssl
import base64
import functools
import re

ssl._create_default_https_context = ssl._create_unverified_context
cookies = {'CONSENT': 'YES+cb.20210720-07-p0.en+FX+410'}

class GNewsEntry:
  def __init__(self, title, link, date_published, source):
    self.title = title
    self.link = link
    self.date_published = date_published
    self.source = source

class NewsEntry:
  def __init__(self, title, article, link, date_published, source):
    self.title = title
    self.article = article
    self.link = link
    self.date_published = date_published
    self.source = source

def getSimilarArticles(url):
    source, title, article = scrapeArticle(url)
    if (source == None or title == None or article == None):
      return []
    query = buildQuery(title, article)
    scrapeGNews(query, source)


def scrapeGNews(query, source):
    query = urllib.parse.quote(query)
    url = BASE_URL + "?q=" + query + "&hl=en-SG&gl=SG&ceid=SG%3Aen"

    feed = feedparser.parse(url)
    entries = parseGNewsRSS(feed)

    return entries

def parseGNewsRSS(feed):
    entries = list(map(parseGNewsEntry, feed['entries']))
    entries = parseNewsEntries(entries)
    return entries

def parseGNewsEntry(entry):
    title = entry['title']
    link = entry['link']
    date_published = entry['published']
    source = entry['source']['title']
    return GNewsEntry(title, link, date_published, source)

def parseNewsEntries(entries):
    news_entries = list()

    for e in entries:
       news_entry = parseNewsEntry(e)
       if (news_entry != None):
          news_entries.append(news_entry)

    for e in news_entries:
       print(e.title)
       print(e.link)

    return news_entries

# TODO: check why certain articles aren't being parsed
def parseNewsEntry(entry):
    if (entry.source.strip() in SUPPORTED_NEWS_SOURCES):
        url = decode_google_news_url(entry.link)
        source, header, article = scrapeArticle(url)
        if (article != None):
          return NewsEntry(header, article, url, entry.date_published, source)
    return None

# TODO: refactor google news URL parsing to utils
_ENCODED_URL_PREFIX = "https://news.google.com/rss/articles/"
_ENCODED_URL_RE = re.compile(fr"^{re.escape(_ENCODED_URL_PREFIX)}(?P<encoded_url>[^?]+)")
_DECODED_URL_RE = re.compile(rb'^\x08\x13".+?(?P<primary_url>http[^\xd2]+)\xd2\x01')

@functools.lru_cache(2048)
def _decode_google_news_url(url: str) -> str:
    match = _ENCODED_URL_RE.match(url)
    encoded_text = match.groupdict()["encoded_url"]  # type: ignore
    encoded_text += "==="  # Fix incorrect padding. Ref: https://stackoverflow.com/a/49459036/
    decoded_text = base64.urlsafe_b64decode(encoded_text)

    match = _DECODED_URL_RE.match(decoded_text)
    primary_url = match.groupdict()["primary_url"]  # type: ignore
    primary_url = primary_url.decode()
    return primary_url


def decode_google_news_url(url: str) -> str:  # Not cached because not all Google News URLs are encoded.
    """Return Google News entry URLs after decoding their encoding as applicable."""
    return _decode_google_news_url(url) if url.startswith(_ENCODED_URL_PREFIX) else url


