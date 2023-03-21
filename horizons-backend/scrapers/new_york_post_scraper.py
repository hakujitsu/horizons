from bs4 import BeautifulSoup as soup, NavigableString
import requests
from utils.constant_utils import REQUEST_HEADER

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

def parseTitle(bsobj):
    header = bsobj.findAll("h1", {"class" : "headline"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()


def parseBody(bsobj):
    bodyContent = bsobj.find_all("div", {"class" : "single__content"})
    if (len(bodyContent) == 0):
        return
    assert(len(bodyContent) == 1)
    bodyContent = bodyContent[0]

    bodyParagraphs = bodyContent.find_all("p", recursive=False)
    if (len(bodyParagraphs) == 0):
        return
    assert(len(bodyParagraphs) > 0)
    bodyParagraphs.pop()

    content = []
    for para in bodyParagraphs:
        content.append(parseParagraph(para).strip())
    content = " ".join(content)
    return content

def parseArticle(nyp_url):
    html=requests.get(nyp_url,headers=REQUEST_HEADER)
    bsobj = soup(html.content,'lxml')
    header = parseTitle(bsobj)
    if (header == None):
        return None, None

    content = parseBody(bsobj)
    if (content == None):
        return None, None

    return header, content