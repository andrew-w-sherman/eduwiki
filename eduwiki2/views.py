from pyramid.view import view_config, view_defaults
from pyramid.response import FileResponse

from urllib import quote, unquote

# html view, gets the html for the index page
@view_config(route_name='index')
def index(request):
    response = FileResponse('templates/index.html', request=request,
        content_type='text/html')
    return response

@view_config(route_name='about')
def about(request):
    response = FileResponse('templates/about.html', request=request,
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
    def user_page(self):
        response = FileResponse('templates/build.html', request=self.request,
            content_type='text/html')
        return response

    # api post, submits user info form and creates a user
    """note: this will need to return stuff"""
    @view_config(route_name='register', request_method='POST', renderer='json')
    def register(self):
        data = self.request.json_body
        return {'success': True, 'user': data['name']}

    # api get, gets the review form for a given topic
    @view_config(route_name='review', request_method='GET', renderer='json')
    def get_review(self):
        topic = unquote(self.request.matchdict['topic'])
        user = unquote(self.request.params["user"])
        return{'success': True, 'done': False, 'name': "Python", 'description': "a great programming language", 'distractors': [{'pagetitle': "Ruby", 'snippet': "a less good programming language"}, {'pagetitle': "AngularJS", 'snippet': "a great framework for front end"}]}

    # api post, posts a review response for a given topic
    @view_config(route_name='review', request_method='POST', renderer='json')
    def submit_review(self):
        topic = unquote(self.request.matchdict['topic'])
        user = self.request.json_body['user']
        review = self.request.json_body['review']
        return {'success': True}

    # api get, gets prereqs for a given topic
    @view_config(route_name='reqs', request_method='GET', renderer='json')
    def get_prereqs(self):
        topic = unquote(self.request.matchdict['topic'])
        prereqs = [{'name': "Science"}, {'name': "Philosophy"}, {'name': "Ontology"}]
        return {'reqs': prereqs, 'success': True}

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
    @view_config(route_name='quiz', request_method='GET', renderer='json')
    def get_quiz(self):
        topic = unquote(self.request.matchdict['topic'])
        return {'success': True, 'name': "Physics", 'definition': "the study of stuff and such", 'distractors': [{'snippet': ""}]}

    # api POST, post quiz choices for database logging
    @view_config(route_name='quiz', request_method='POST', renderer='json')
    def submit_quiz(self):
        topic = unquote(self.request.matchdict['topic'])

    # api GET, for a given topic get the info writeup
    @view_config(route_name='info', request_method='GET', renderer='json')
    def get_info(self):
        topic = unquote(self.request.matchdict['topic'])
