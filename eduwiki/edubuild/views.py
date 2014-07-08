from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from urllib import quote, unquote
import os, sys
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from diagnose import query
from wikipedia import DisambiguationError

def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('edubuild/index.html', context_dict, context)

def build(request, build_name_url=None):
    context = RequestContext(request)
    context_dict = {}
    build_name = build_name_url.replace('_', ' ')
    try:
        json_tree = query(build_name)  # comes out in a JSON string
    except DisambiguationError as dis:
        return disambiguation(request, dis)
    context_dict['topic'] = json.loads(json_tree, object_hook=recurhook)
    return render_to_response('edubuild/build.html', context_dict, context)

def disambiguation(request, dis=[]):
    if not dis:
        return redirect('index')
    pages = [{'title': option, 'text': description, 'link': link}
             for option, description, link in
             zip(dis.options, dis.descriptions, dis.links)]
    context_dict = {'pages': pages}
    context = RequestContext(request)
    return render_to_response('edubuild/disambiguation.html',
                              context_dict, context)
    

#extra code for json decoding
def recurhook(d):
    if d.get('children', False):
        # d['children'] = json.loads(d['children'], recurhook)
        children = []
        for child in d['children']:
            children.append(json.loads(child, object_hook=recurhook))
        d['children'] = children
    return d