from bs4 import BeautifulSoup as soup, NavigableString
import requests
from datetime import date
today = date.today()
d = today.strftime("%m-%d-%y")
bbc_url="https://www.bbc.com/news/world-us-canada-64883668"
html = requests.get(bbc_url)
bsobj = soup(html.content,'lxml')

def parseNestedTag(t):
    tagText = ""
    for txt in t.contents:
        if (isinstance(txt, NavigableString)):
            tagText += txt
        else:
            tagText += parseNestedTag(txt)
    return tagText

def parseParagraph(p):
    paragraphText = ""
    for txt in p.contents:
        if (isinstance(txt, NavigableString)):
            paragraphText += txt
        else:
            paragraphText += parseNestedTag(txt)
    return paragraphText

def parseTitle():
    header = bsobj.findAll("h1", {"id" : "main-heading"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()


def parseBody():
    bodyParagraphs = bsobj.find_all("div", {"data-component" : "text-block"})
    if (len(bodyParagraphs) == 0):
        return

    content = []
    for para in bodyParagraphs:
        if (len(para.contents) == 1 and para.contents[0].name == "a"):
            continue
        content.append(parseParagraph(para).strip())
    content = "\n".join(content)
    return content

def parseArticle():
    header = parseTitle()
    if (header == None):
        return

    content = parseBody()
    if (content == None):
        return

    print(header)
    print()
    print(content)

parseArticle()