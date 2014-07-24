from cache import cache, fetch
from pattern.web import Wikipedia, Element
from pattern.search import match, Pattern
from pattern.en import parsetree
wiki = Wikipedia()

# Retrieves the review information for the Build API and caches it.
# Returns a dict w/ name, description, and distractors, which is a list of
# dicts w/ pagetitle and snippet.
def review(topic):
    name = topic+" review"
    fetched = fetch(name)
    if fetched:
        return fetched
    art = wiki.search(topic)
    rev = {}
    if art.disambiguation:
        raise DisambiguationError()
    rev['name'] = art.title
    rev['description'] = getDescription(art)
    rev['distractors'] = getDists(art)
    cache(name, rev)
    return rev

# Retrieves the prereq info for the Build API and caches it, then caches the
# prerequisite pages and their reviews. Returns a list of dicts w/ name.
def prereqs(topic):
    name = topic+" prereqs"
    fetched = fetch(name)
    if fetched:
        return fetched
    art = wiki.search(topic)
    reqs = getReqs(art)
    for req in reqs:
        review(req) # without grabbing return, works as pure caching function
    cache(name, reqs)
    return reqs

# Retrieves the quiz info for the Learn API and caches it, then caches the
# info page on the topic. Returns a dict w/ name, definition, distractors,
# which is a list of dicts w/ snippet and pagetitle, and prereqs, which
# is a list of strings.
def quiz(topic):
    name = topic+" quiz"
    fetched = fetch(name)
    if fetched:
        return fetched
    art = wiki.search(topic)
    quiz = {}
    quiz['name'] = art.title
    quiz['description'] = getDescription(art)
    quiz['distractors'] = getDists(art)
    quiz['prereqs'] = getReqs(art)
    cache(name, quiz)
    return quiz

# Retrieves the info writeup for the Learn API and caches it. Returns a dict
# w/ name and text.
def info(topic):
    name = topic+" info"
    fetched = fetch(name)
    if fetched:
        return fetched
    art = wiki.search(topic)
    info = {}
    info['name'] = art.title
    info['text'] = art.sections[0].string
    cache(name, info)
    return info

# Retrieves a long list of the prerequisites for the prereq API and caches it.
# Returns a dict w/ name and reqs, which is a list of dicts w/ name.
def reqsLong(topic):
    name = topic+" longreqs"
    fetched = fetch(name)
    if fetched:
        return fetched
    art = wiki.search(topic)
    reqs = getLongReqs(art)
    return {'name': art.title, 'reqs': reqs}


def getDists(article):
    dists = []
    links = sectionLinks(article, 0)
    i = 0
    while len(dists) < 3:
        if i >= len(links):
            break
        child = wiki.search(links[i][0])
        if 10 < len(child.links) < 500:
            dists.append(child)
        i += 1
    return [{'pagetitle': art.title, 'snippet': getDescription(art)}
             for art in dists]


# returns an article description using NLP from pattern
def getDescription(article):
    intro = parsetree(article.sections[0].string, lemmata=True)
    pattern = Pattern.fromstring('be DT *+')
    try:
        mat = pattern.match(intro)
        return mat.string
    except TypeError:
        pattern = Pattern.fromstring('be *+')
        return pattern.match(intro).string

def getReqs(article):
    reqs = []
    links = sectionLinks(article, 0)
    i = 0
    while len(reqs) < 3:
        if i >= len(links):
            break
        child = wiki.search(links[i][0])
        if 10 < len(child.links) < 500:
            reqs.append(child)
        i += 1
    return [art.title for art in reqs]

def getLongReqs(article):
    links = sectionLinks(article, 0)
    reqs = [wiki.search(link[0]) for link in links]
    return [{'name': art.title} for art in reqs]


# returns section links (stripping infoboxes/other non-content links) for the
# section with a given section number, as an ordered list of tuples of format:
# (actual link name, name used in the text)
def sectionLinks(article, section_number):
    section = Element(article.sections[section_number].source)
    link_elements = section('p > a')
    links = []
    for elem in link_elements:
        href = elem.attrs['href'].split('/')[-1].replace('_', ' ').split('#')[0]
        href = href.replace('&#160;', ' ')
        link = (href, elem.content)
        links.append(link)
    return links
