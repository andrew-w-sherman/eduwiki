from bs4 import BeautifulSoup
import wikipedia
import requests
import urllib

class Article(object):
    """Represents a wikipedia article"""
    def __init__(self, title):
        if not title:
            raise Exception
        
        url = urllib.quote(title)
        url = "http://en.wikipedia.org/wiki/"+url
        html = requests.get(url)
        soup = BeautifulSoup(html)
        
        
