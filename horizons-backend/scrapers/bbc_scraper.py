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
    header = bsobj.findAll("h1", {"id" : "main-heading"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()


def parseBody(bsobj):
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

def parseArticle(bbc_url):
    html=requests.get(bbc_url,headers=REQUEST_HEADER)
    bsobj = soup(html.content,'lxml')
    header = parseTitle(bsobj)
    if (header == None):
        return None, None

    content = parseBody(bsobj)
    if (content == None):
        return None, None

    return header, content

