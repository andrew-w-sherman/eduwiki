from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from diagnose import query

def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('edubuild/index.html', context_dict, context)

def build(request):
    context = RequestContext(request)
    context_dict = {'topic': {'title': "Python Django"},
                    'prereqs': [
                        {'title': "Python", 'definition': "a great programming language", 'distractors': [{'pagetitle': "Ruby", 'snippet': "a less good programming language"}]}
                    ],
                    'root': {'title': "The root", 'children': [{'title': "Child One", 'children': []},{'title': "Child Two", 'children': [{'title': "Child Three", 'children': []}]}]}}
    return render_to_response('edubuild/build.html', context_dict, context)