from bs4 import BeautifulSoup as soup, NavigableString
import requests

newsweek_url="https://www.newsweek.com/republican-divide-widens-over-debt-limit-senate-opts-bipartisanship-1786715"
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
html=requests.get(newsweek_url,headers=header)

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
    header = bsobj.findAll("h1", {"class" : "title"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()

def parseBody():
     # Get body text
    bodyContent = bsobj.find_all("div", {"class" : "article-body"})
    if (len(bodyContent) == 0):
        return
    assert(len(bodyContent) == 1)
    bodyContent = bodyContent[0]

    bodyParagraphs = bodyContent.find_all("p", recursive=False)
    if (len(bodyParagraphs) == 0):
        return
    assert(len(bodyParagraphs) > 0)

    content = []
    for para in bodyParagraphs:
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
