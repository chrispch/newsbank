import requests
import json
from bs4 import BeautifulSoup

news_providers = {"TODAY": {
                    "Singapore": "https://www.todayonline.com/singapore", 
                    "World": "https://www.todayonline.com/api/v3/news_feed/5?items=8"
                    },
                  "BBC": {
                      "World": "http://www.bbc.com/news/world"
                  }    
                }

def get_news(site, category):
    url = news_providers[site][category]
    r = requests.get(url)
    c = r.content.decode('utf-8')
    if site == "TODAY":
        # c = c.replace('\\u2019', '\'').replace('\\u2019', '\'').replace('\\', '')
        news_list = json.loads(c, encoding='utf-8')
        for news_item in news_list["nodes"]:
            title = news_item["node"]["title"]
            abstract = news_item["node"]["abstract"]
            node_url = news_item["node"]["node_url"]
            date = news_item["node"]["published_date"]
            author = news_item["node"]["author"]
            if author == []:
                author = "-"
            else:
                author = author[0]["name"]

    elif site == "BBC":
        soup = BeautifulSoup(c)
        # soup.find_all("div", {"id": "comp-pattern-library-5"})

get_news("TODAY", "World")