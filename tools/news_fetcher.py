from utils import NEWS_API_KEY
import requests
from langchain.tools import tool
import json

@tool
def fetch_news(query:str, language="en", page_size=3):
    """ News api to fetch recent news from given news query"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": language,
        "pageSize": page_size,
        "sortBy": "publishedAt"
    }
    response = requests.get(url, params=params)
    #print(json.dumps(response.json(), indent=2))
    with open("validation/news.json","w",encoding="utf-8") as file:
        file.write(json.dumps(response.json(), indent=2))
    articles = response.json().get("articles", [])
    return [{"title": a["title"], "url": a["url"], "content": a["description"]} for a in articles]
