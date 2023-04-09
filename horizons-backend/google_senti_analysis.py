# Imports the Google Cloud client library
from google.cloud import language_v1
import aiohttp
import asyncio
from utils.constant_utils import REQUEST_HEADER

"""
Analyses the entity sentiment of a given text.

Parameters:
    text_content: The text (in the form of a string containing no special characters) to analyse.

Returns a response object.
"""
def analyze_entity_sentiment(text_content):
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.types.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    return response

def getEntitySentimentsForArticles(article_list):
    asyncio.run(asyncGetEntitySentiment(article_list))
    return article_list

async def asyncGetEntitySentiment(article_list):
    tasks = [
    getEntitySentiment(article)
        for article in article_list
    ]
    return await asyncio.gather(*tasks)

async def getEntitySentiment(article):
    print(article.title)
    text_content = article.article
    client = language_v1.LanguageServiceClient()

# Available types: PLAIN_TEXT, HTML
    type_ = language_v1.types.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    article.setEntitySentiment(response)

    print("response for " + article.title + " done")

    return article