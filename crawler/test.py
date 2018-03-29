import requests
import json

r = requests.get('http://127.0.0.1:5000/articles?where={ "site": "BBC" }&page=3&sort=[("date_seconds", -1)]').json()
for i in r["_items"]:
    print(i["date_seconds"])