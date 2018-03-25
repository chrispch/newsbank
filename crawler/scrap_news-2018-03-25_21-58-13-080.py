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
                                        "full_text": {
                                            "from_article":True,
                                            "class":"article-detail_body"
                                        },
                                        "abstract": {
                                            "from_article":True
                                        },
                                        "date_seconds": {
                                            "from_article":False,
                                            "tag":"pubdate"
                                        },
                                        "author":{
                                            "from_article":True
                                        }
                                    }
                                },
                                "BBC": {
                                    "Default": {
                                        "full_text": {
                                            "from_article":True,
                                            "class":"story-body__inner"
                                        },
                                        "abstract": {
                                            "from_article":False,
                                            "class":"div"
                                        },
                                        "date_seconds": {
                                            "from_article":True,
                                            "class":"date",
                                            "attr":"data-seconds"
                                        },
                                        "author":{
                                            "from_article":True
                                        }
                                    }
                                },
                                "Guardian": {
                                    "Default": {
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
                                            "tag":"pubdate"
                                        },
                                        "author": {
                                            "from_article":False,
                                            "class":"dc:creator"
                                        }
                                    },
                                }

                            }

def get_news(site, category):
    url = news_providers[site][category]
    c = requests.get(url).content
    soup = BeautifulSoup(c, "lxml")
    print(soup.prettify())
    news_items = soup.find_all("item")
    for news in news_items:
        # get title
        title = news.find("title").text
        # get article link
        href = news.get("link")
        print(href)
        if "https" not in href:
            href = url + "/" + href

        # get article html
        article = BeautifulSoup(requests.get(href).content, "html.parser")
        # print(article.prettify)
        # check if there are special scrap instructions for current category
        if category not in special_scrap_instructions[site]:
            i = special_scrap_instructions[site]["Default"]
        else:
            i = special_scrap_instructions[site][category]
        
        # get date_seconds
        date = parse_instructions(i["date_seconds"], news, article).text
        try:
            dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            dt = float(date)
        date_seconds = dt.timestamp()
        # print(date_seconds)

        # get abstract
        abstract_soup = BeautifulSoup(parse_instructions(i["abstract"], news, article).text, "html.parser")
        abstract = abstract_soup.find("p").text
        # print(abstract)

        # get article text
        article_body = parse_instructions(i["full_text"], news, article)
        paragraphs = article_body.find_all("p")
        full_text = ""
        for p in paragraphs:
            full_text = full_text + p
        # print(full_text)

def save_article(site, category, title, abstract, full_text, date_seconds, author, href):
    pass

def parse_instructions(i, news_ref, article_ref):
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
        search = {"class": i["class"]}
        results = _ref.find(class_=i["class"])
    if "attr" in i:
        return results[i["attr"]]
    else:
        # print(results)
        return results



get_news("Guardian", "World")