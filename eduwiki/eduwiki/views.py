from django.shortcuts import render, render_to_response
from django.template import RequestContext

def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('EduWiki/index.html', context_dict, context)
