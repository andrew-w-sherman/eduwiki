from pyramid.view import view_config, view_defaults
from pyramid.response import FileResponse

from urllib import quote, unquote

from Wiki import review, prereqs, quiz, info, reqsLong

# html view, gets the html for the index page
@view_config(route_name='index')
def index(request):
    response = FileResponse('templates/index.html', request=request,
        content_type='text/html')
    return response

@view_config(route_name='about')
def about(request):
    response = FileResponse('sketches/recurse_sketch.html', request=request,
        content_type='text/html')
    return response

@view_config(route_name='contact')
def contact(request):
    response = FileResponse('templates/contact.html', request=request,
        content_type='text/html')
    return response


# views for build page
@view_defaults(route_name='build')
class BuildViews:
    def __init__(self, request):
        self.request = request

    # html view, gets the html for the build page
    @view_config(request_method='GET')
    def build_page(self):
        response = FileResponse('templates/build.html', request=self.request,
            content_type='text/html')
        return response

    # api post, submits user info form and creates a user
    """returns success, errors, user, user.unknown..."""
    @view_config(route_name='register', request_method='POST', renderer='json')
    def register(self):
        data = self.request.json_body
        return {'success': True, 'user': data['name']}

    # api get, gets the review form for a given topic
    """returns success, errors, errors.disambig, done, name, description,
    distractors[i].snippet, distractors[i].pagetitle"""
    @view_config(route_name='review', request_method='GET', renderer='json')
    def get_review(self):
        print("In get review")
        topic = unquote(self.request.matchdict['topic'])
        user = unquote(self.request.params["user"])
        rev = review(topic)
        rev['success'] = True
        return rev

    # api post, posts a review response for a given topic
    """returns success, errors"""
    @view_config(route_name='review', request_method='POST', renderer='json')
    def submit_review(self):
        topic = unquote(self.request.matchdict['topic'])
        user = self.request.json_body['user']
        review = self.request.json_body['review']
        return {'success': True}

    # api get, gets prereqs for a given topic
    """returns success, errors, prereqs[i].name"""
    @view_config(route_name='reqs', request_method='GET', renderer='json')
    def get_prereqs(self):
        topic = unquote(self.request.matchdict['topic'])
        reqs = prereqs(topic)
        reqs['success'] = True
        return reqs


# views for learn page
@view_defaults(route_name='learn')
class LearnViews:
    def __init__(self, request):
        self.request = request

    # html view, gets the html for the learn page
    @view_config(request_method='GET')
    def learn_page(self):
        response = FileResponse('templates/learn.html', request=self.request,
            content_type='text/html')
        return response

    # api GET, for a specified topic get the quiz info
    """returns success, errors, name, definition, distractors[i].snippet,
    distractors[i].pagetitle, prereqs[i]"""
    @view_config(route_name='quiz', request_method='GET', renderer='json')
    def get_quiz(self):
        topic = unquote(self.request.matchdict['topic'])
        qu = quiz(topic)
        qu['success'] = True
        return qu

    # api POST, post quiz choices for database logging
    """currently unused, returns success, errors"""
    @view_config(route_name='quiz', request_method='POST', renderer='json')
    def submit_quiz(self):
        topic = unquote(self.request.matchdict['topic'])

    # api GET, for a given topic get the info writeup
    """returns success, errors, writeup.name, writeup.text"""
    @view_config(route_name='info', request_method='GET', renderer='json')
    def get_info(self):
        topic = unquote(self.request.matchdict['topic'])
        inf = {}
        inf['writeup'] = info(topic)
        inf['success'] = True
        return inf


@view_defaults(route_name='prereqs')
class PrereqViews:
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def prereq_page(self):
        response = FileResponse('templates/prereq.html', request=self.request,
                                content_type='text/html')
        return response

    @view_config(route_name='prereqstart', request_method='GET', renderer='json')
    def prereq_start(self):
        topic = 'Support Vector Machines'
        return reqsLong(topic)

    @view_config(route_name='next_req', request_method='POST', renderer='json')
    def prereq_next(self):
        topic = unquote(self.request.matchdict['topic'])
        body = self.request.json_body
        return reqsLong()
