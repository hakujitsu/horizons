from bs4 import BeautifulSoup as soup, NavigableString
import requests
cnbc_url="https://www.cnbc.com/2023/03/09/west-virginia-to-ask-supreme-court-to-allow-transgender-girls-sports-ban.html"
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
html=requests.get(cnbc_url,headers=header)
bsobj = soup(html.content,'lxml')

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

def parseTitle():
    # Get title
    header = bsobj.findAll("h1", {"class" : "ArticleHeader-headline"})
    if (len(header) < 1):
        return
    assert(len(header) == 1)
    return parseNestedTag(header[0]).strip()

def parseBody():
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
