import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, time
from pymongo import MongoClient, DESCENDING, TEXT

provider_json = os.path.dirname(os.path.realpath(__file__)) + "/news_providers.json"
instructions_json = os.path.dirname(os.path.realpath(__file__)) + "/instructions.json"
password_txt = os.path.dirname(os.path.realpath(__file__)) + "/password.txt"
database = "newsbank"
collection = "articles"

# returns MongoClient collection
def get_db(database, collection, username, password, port="27017", host="localhost"):
    uri = "mongodb://{}:{}@{}:{}/{}".format(username, password, host, port, database)
    client = MongoClient(uri)
    db = client[database]
    collection = db[collection]
    return collection

# create Mongo indexes
def create_indexes(db):
    db.create_index([("full_text", TEXT), ("title", TEXT)])
    db.create_index([("date_seconds", DESCENDING)])
    # print(db.index_information())

# scraps news on a given site and category
def get_news(site, category, db):
    url = news_providers[site][category]
    c = requests.get(url).content
    soup = BeautifulSoup(c, "xml")
    news_items = soup.find_all("item")
    for news in news_items:
        
        # get title
        title = news.find("title").text

        # get article link
        href = news.find("link").text
        if "http" not in href:
            href = "http://" + href
        
        # check if article already in db
        if db.find_one({"href": href}) is not None:
            # if article exists, all articles later than the current one already exist in db
            break

        # get scrapping instructions
        if category not in instructions[site]:
            # check if there are special scrap instructions for current category
            i = instructions[site]["Default"]
        else:
            i = instructions[site][category]

        # get article html/json
        if i["article"]["cdn"]:
            article_id = news.find("guid").text.split(" ")[0]
            _href = i["article"]["base_url"].format(article_id)
            article = requests.get(_href).json()
        else:
            _href = i["article"]["base_url"].format(href)
            article = BeautifulSoup(requests.get(_href).content, "html.parser") 
        
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

        # get abstract
        if not i["article"]["cdn"]:
            abstract_soup = BeautifulSoup(parse_instructions(i["abstract"], news, article).text, "html.parser")
        else:
            abstract_soup = BeautifulSoup(parse_instructions(i["abstract"], news, article), "html.parser")
        if abstract_soup.find("p") == None:
            abstract = abstract_soup.text
        else:
            abstract = abstract_soup.find("p").text

        # get article text
        if not i["article"]["cdn"]:
            article_body = parse_instructions(i["full_text"], news, article)
        else:
            article_body = BeautifulSoup(parse_instructions(i["full_text"], news, article), "html.parser")
        if article_body != None:
            paragraphs = article_body.find_all("p")
            full_text = ""
            for p in paragraphs:
                full_text = full_text + p.text + "\n"
        else:
            full_text = None

        # get author
        author = parse_instructions(i["author"], news, article)
        if author != None and not i["article"]["cdn"]:
            author = author.text
        
        save_article(site, category, title, abstract, full_text, date_seconds, author, href, db)

def save_article(site, category, title, abstract, full_text, date_seconds, author, href, db):
    article = {
        "site": site,
        "category": category,
        "title": title,
        "abstract": abstract,
        "full_text": full_text,
        "date_seconds": date_seconds,
        "author": author,
        "href": href
    }
    # print(article)
    db.insert_one(article)

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


###################################################
# Main
###################################################


# load jsons
with open(provider_json, "r") as f:
    news_providers = json.load(f)

with open(instructions_json, "r") as f:
    instructions = json.load(f)

# get mongo auth credentials
with open (password_txt , 'r') as pw:
    global username, password
    read = pw.readline().rstrip().split(":")
    username = read[0]
    password = read[1]

articles_db = get_db(database, collection, username, password)
create_indexes(articles_db)
for site in news_providers:
    for category in news_providers[site]:
        get_news(site, category, articles_db)
