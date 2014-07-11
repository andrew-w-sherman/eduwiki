from pattern.web import Wikipedia
from eduprototype.models import WikiPage, Link

wiki = Wikipedia()

# main front facing method, takes a search term and returns the model from the
# database, either an article or a disambiguation
def query(search_term):
    article = WikiPage.objects.get(pk=search_term, False)
    if not article or not article.valid:
        page = wiki.search(search_term)
        link_mods = []
        for link in page.sections[0].links:
            child = wiki.search(link)
            link_mods.append(WikiPage(title=child.title, top_section= valid = False))
        article = WikiPage(title=page.title, links=link_mods,
            wikitext = page.string, top_section = page.sections[0].string
            disambiguation = page.disambiguation, valid = True)
        article.save()
    return article
        