from pattern.web import Wikipedia
from eduprototype.models import WikiPage, Link

wiki = Wikipedia()

# main front facing method, takes a search term and returns the model from the
# database
def query(search_term, children = 3):
    if children > 10:
        children = 10
    
    article = WikiPage.objects.get(pk=search_term, False)
    if not article:
        article = wiki.search(search_term)
        if article.disambiguation
    elif article.disambiguation:
        