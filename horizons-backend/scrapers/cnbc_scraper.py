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

def parseGroup(g):
    p = g.find_all("p", recursive=False)
    paragraphs = []
    for txt in p:
        paragraphText = ""
        if (isinstance(txt, NavigableString)):
            paragraphText += txt
        else:
            paragraphText += parseNestedTag(txt)
        paragraphs.append(paragraphText)
    return paragraphs

def parseTitle(bsobj):
    # Get title
    header = bsobj.findAll("h1", {"class" : "ArticleHeader-headline"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()

def parseBody(bsobj):
     # Get body text
    bodyContent = bsobj.find_all("div", {"class" : "ArticleBody-articleBody"})
    if (len(bodyContent) == 0):
        return
    assert(len(bodyContent) == 1)
    bodyContent = bodyContent[0]

    bodyGroups = bodyContent.find_all("div", {"class" : "group"})
    if (len(bodyGroups) == 0):
        return
    assert(len(bodyGroups) > 0)

    content = []
    for group in bodyGroups:
        content = content + parseGroup(group)

    content = " ".join(content)
    return content

def parseArticle(cnbc_url):
    html=requests.get(cnbc_url,headers=REQUEST_HEADER)
    bsobj = soup(html.content,'lxml')
    header = parseTitle(bsobj)
    if (header == None):
        return None, None

    content = parseBody(bsobj)
    if (content == None):
        return None, None

    return header, content
