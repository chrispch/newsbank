import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, time

news_providers = {  "TODAY": {
                        "Hot News": "http://www.todayonline.com/hot-news/feed",
                        "Singapore": "http://www.todayonline.com/feed/singapore", 
                        "World": "http://www.todayonline.com/feed/world"
                    },
                    "BBC": {
                        "World": "http://feeds.bbci.co.uk/news/world/rss.xml"
                    },
                    "Guardian": {
                        "World": "https://www.theguardian.com/world/rss"
                    }

                }
api_url = "http://127.0.0.1:5000/"

special_scrap_instructions = {  "TODAY": {
                                    "Default": {
                                        "article": {
                                            "cdn":True,
                                            "base_url": "https://www.todayonline.com/api/v3/article/{}?tid=3"
                                        }, 
                                        "full_text": {
                                            "from_article":True,
                                            "json":["node", "body"]
                                        },
                                        "abstract": {
                                            "from_article":True,
                                            "json":["node", "body"]
                                        },
                                        "date_seconds": {
                                            "from_article":False,
                                            "tag":"pubDate"
                                        },
                                        "author":{
                                            "from_article":True,
                                            "json":["node", "author", 0, "name"]
                                        }
                                    }
                                },
                                "BBC": {
                                    "Default": {
                                        "article": {
                                            "cdn":False,
                                            "base_url": "{}"
                                        }, 
                                        "full_text": {
                                            "from_article":True,
                                            "class":"story-body__inner"
                                        },
                                        "abstract": {
                                            "from_article":False,
                                            "tag":"description"
                                        },
                                        "date_seconds": {
                                            "from_article":False,
                                            "tag":"pubDate"
                                        },
                                        "author":None
                                    }
                                },
                                "Guardian": {
                                    "Default": {
                                        "article": {
                                            "cdn":False,
                                            "base_url": "{}"
                                        }, 
                                        "full_text": {
                                            "from_article":True,
                                            "class":"content__article-body"
                                        },
                                        "abstract": {
                                            "from_article":False,
                                            "tag":"description"
                                        },
                                        "date_seconds": {
                                            "from_article":False,
                                            "tag":"pubDate"
                                        },
                                        "author": {
                                            "from_article":False,
                                            "tag":"dc:creator"
                                        }
                                    },
                                }
                            }

def get_news(site, category):
    url = news_providers[site][category]
    c = requests.get(url).content
    soup = BeautifulSoup(c, "xml")
    # print(soup.prettify())
    news_items = soup.find_all("item")
    for news in news_items:
        # get title
        title = news.find("title").text
        print(title)

        # get article link
        href = news.find("link").text
        if "http" not in href:
            href = "http://" + href
        print(href)

        # check if there are special scrap instructions for current category
        if category not in special_scrap_instructions[site]:
            i = special_scrap_instructions[site]["Default"]
        else:
            i = special_scrap_instructions[site][category]

        # get article html/json
        if i["article"]["cdn"]:
            article_id = news.find("guid").text.split(" ")[0]
            _href = i["article"]["base_url"].format(article_id)
            article = requests.get(_href).json()
        else:
            _href = i["article"]["base_url"].format(href)
            article = BeautifulSoup(requests.get(_href).content, "html.parser") 
        print(_href)
        
        # get date_seconds
        date = parse_instructions(i["date_seconds"], news, article)
        try:
            dt = datetime.strptime(date.text, "%a, %d %b %Y %H:%M:%S %z")
            date_seconds = dt.timestamp()
        except ValueError:
            dt = datetime.strptime(date.text, "%a, %d %b %Y %H:%M:%S %Z")
            date_seconds = dt.timestamp()
        except AttributeError:
            date_seconds = float(date)
        
        print(date_seconds)

        # get abstract
        if not i["article"]["cdn"]:
            abstract_soup = BeautifulSoup(parse_instructions(i["abstract"], news, article).text, "html.parser")
        else:
            abstract_soup = BeautifulSoup(parse_instructions(i["abstract"], news, article), "html.parser")
        if abstract_soup.find("p") == None:
            abstract = abstract_soup.text
        else:
            abstract = abstract_soup.find("p").text
        print(abstract)

        # get article text
        if not i["article"]["cdn"]:
            article_body = parse_instructions(i["full_text"], news, article)
        else:
            article_body = BeautifulSoup(parse_instructions(i["full_text"], news, article))
        if article_body != None:
            paragraphs = article_body.find_all("p")
            full_text = ""
            for p in paragraphs:
                full_text = full_text + p.text + "\n"
        else:
            full_text = None

        
        print(full_text)

        # get author
        author = parse_instructions(i["author"], news, article)
        if author != None and not i["article"]["cdn"]:
            author = author.text
        print(author)

def save_article(site, category, title, abstract, full_text, date_seconds, author, href):
    pass

def parse_instructions(i, news_ref, article_ref):
    if i == None:
        return None
    if i["from_article"]:
        _ref = article_ref
    else:
        _ref = news_ref
    if "tag" in i and "class" in i:
        search = '{}, \{"class":{}\}'.format(i["tag"], i["class"])
        results = _ref.find(search)
    elif "tag" in i:
        search = i["tag"]
        results = _ref.find(search)
    elif "class" in i:
        # print(i["class"])
        # print(article_ref)
        results = _ref.find(class_=i["class"])
    elif "json" in i:
        results = article_ref
        for node in i["json"]:
            try:
                results = results[node]
            except IndexError:
                results = None
                break
    if "attr" in i:
        # print(results)
        return results[i["attr"]]
    else:
        # print(results)
        return results



get_news("BBC", "World")