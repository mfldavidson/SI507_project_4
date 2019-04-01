import json

def open_cache(CACHEFILE):
    try:
        with open(CACHEFILE,'r') as cache_file:
            cache_json = file.read()
            cache_diction = json.loads(cache_json)
    except:
        cache_diction = {}
    return cache_diction

def cache_data(CACHEFILE,url,cache_diction,new_data):
    with open(CACHEFILE,'w') as cache_file:
        cache_diction[url] = new_data
        cache_json = json.dumps(cache_diction)
        cache_file.write(cache_json)
