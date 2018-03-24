import requests
import json
from bs4 import BeautifulSoup

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
    r = requests.get(url)
    c = r.content.decode('utf-8')
    if site == "TODAY":
        # c = c.replace('\\u2019', '\'').replace('\\u2019', '\'').replace('\\', '')
        news_list = json.loads(c, encoding='utf-8')
        for news_item in news_list["nodes"]:
            title = news_item["node"]["title"]
            if requests.get(api_url + 'articles?where={"title":"' + title + '"}').json()["_items"] == []:
                abstract = news_item["node"]["abstract"]
                node_url = news_item["node"]["node_url"]
                node_id = news_item["node"]["node_id"]
                date = news_item["node"]["publication_date"]
                author = news_item["node"]["author"]
                article = requests.get("https://www.todayonline.com/api/v3/article/{}?tid=3".format(node_id)).content.decode('utf-8')
                full_text = json.loads(article, encoding='utf-8')["node"]["body"]
                if author == []:
                    author = "-"
                else:
                    author = author[0]["name"]


    elif site == "BBC":
        soup = BeautifulSoup(c)
        # soup.find_all("div", {"id": "comp-pattern-library-5"})

get_news("TODAY", "World")