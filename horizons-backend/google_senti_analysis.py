# Imports the Google Cloud client library
from google.cloud import language_v1

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
