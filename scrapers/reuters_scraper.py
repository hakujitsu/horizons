from bs4 import BeautifulSoup as soup, NavigableString
import requests
from datetime import date
today = date.today()
d = today.strftime("%m-%d-%y")
reuters_url="https://www.reuters.com/world/studying-ukraine-war-chinas-military-minds-fret-over-us-missiles-starlink-2023-03-08/"
html = requests.get(reuters_url)
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
    # Get title
    header = bsobj.findAll("h1", {"data-testid" : "Heading"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()

def parseBody():
    # Get body text
    bodyParagraphs = []

    index = 0
    hasMoreParagraphs = True
    while(hasMoreParagraphs):
        tagName = "paragraph-" + str(index)
        tag = bsobj.find("p", {"data-testid" : tagName})
        if (tag == None):
            break
        index += 1
        bodyParagraphs.append(tag)

    content = []
    for para in bodyParagraphs:
        if (len(para.contents) == 1 and para.contents[0].name == "a"):
            continue
        content.append(parseParagraph(para).strip())
    content = " ".join(content)
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
