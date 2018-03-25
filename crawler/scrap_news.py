import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, time

news_providers = {"TODAY": {
                    "Singapore": "https://www.todayonline.com/api/v3/news_feed/3?items=8", 
                    "World": "https://www.todayonline.com/api/v3/news_feed/5?items=8"
                    },
                  "BBC": {
                      "World": "http://www.bbc.com/news/world"
                  }    
                }
api_url = "http://127.0.0.1:5000/"

def get_news(site, category):
    url = news_providers[site][category]
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    c = r.content.decode('utf-8')
    if site == "TODAY":
        # c = c.replace('\\u2019', '\'').replace('\\u2019', '\'').replace('\\', '')
        news_list = json.loads(c, encoding='utf-8')
        for news_item in news_list["nodes"]:
            title = news_item["node"]["title"]
            # get from API provider to check if article already exists in database
            if requests.get(api_url + 'articles?where={"title":"' + title + '"}').json()["_items"] == []:
                abstract = news_item["node"]["abstract"]
                node_url = news_item["node"]["node_url"]
                node_id = news_item["node"]["node_id"]
                date = news_item["node"]["publication_date"]
                dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                date_seconds = dt.timestamp()
                author = news_item["node"]["author"]
                article = requests.get("https://www.todayonline.com/api/v3/article/{}?tid=3".format(node_id)).content.decode('utf-8')
                full_text = json.loads(article, encoding='utf-8')["node"]["body"]
                if author == []:
                    author = "-"
                else:
                    author = author[0]["name"]


    elif site == "BBC":
        soup = BeautifulSoup(c, "html.parser")
        # Buzzard
        buzzard = soup.find("div", {"class": "buzzard-item"})
        abstract = buzzard.find("p", {"class": "buzzard__summary"}).text
        title = buzzard.find("a").text
        data_seconds = float(buzzard.find("div", {"class": "date"})["data-seconds"])
        href = "https://bbc.com" + buzzard.find("a").get("href")
        # print(title, abstract, href, data_seconds)
        # Pigeon
        pigeon_items = soup.find("div", {"class": "pigeon"}).find_all("div", {"class": "pigeon-item"})
        for item in pigeon_items:
            body = item.find("div", {"class": "pigeon-item__body"})
            if body:
                abstract = body.find("p").text
            else:
                abstract = ""
                body = item
            title = body.find("a").text
            href = "https://bbc.com" + body.find("a").get("href")
            data_seconds = float(body.find("div", {"class": "date"})["data-seconds"])
            # print(title, abstract, href, data_seconds)
        # Macaw
        macaw_items = soup.find("div", {"class": "macaw"}).find_all("div", {"class": "macaw-item"})
        for item in macaw_items:
            body = item.find("div", {"class": "macaw-item__body"})
            title = body.find("a").text
            abstract = ""
            href = "https://bbc.com" + body.find("a").get("href")
            data_seconds = float(body.find("div", {"class": "date"})["data-seconds"])
            print(title, abstract, href, data_seconds)

def save_article(site, category, title, abstract, full_text, date_seconds, author, href):
    


get_news("TODAY", "World")