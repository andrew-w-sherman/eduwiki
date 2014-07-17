import os
# uses ../../Cache/ as the cache directory
cache_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Cache")
import hashlib
from urllib import quote
from pickle import dump, load
from time import time
max_age = 864000 # 10 days

# caches a python object under a specified name with pickle, unless there is
# something already cached under that name that is less than max_age seconds
# old (currently hardcoded to 10 days)
def cache(name, obj):
    path = os.path.join(cache_path, hashlib.sha1(name.encode('utf8')).hexdigest())
    if os.path.isfile(path):
        age = time() - os.path.getmtime(path)
        if age < max_age:
            return
    with open(path, 'w') as file:
        dump(obj, file)

# fetches a python object under a specified name with pickle, returns false if
# it's not in the cache
def fetch(name):
    path = os.path.join(cache_path, hashlib.sha1(name.encode('utf8')).hexdigest())
    if not os.path.isfile(path):
        return False
    with open(path, 'r') as file:
        return load(file)
