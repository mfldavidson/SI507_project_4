from bs4 import BeautifulSoup
import requests, json
from setup import *
from caching import *

BASEURL = "https://www.nps.gov"

# set up cache and get data out of cache or create empty dictionary
CACHEFILE = "nps_cache.json"

cache_diction = open_cache(CACHEFILE)

# try to get the data out of the dictionary; if not, make a request to get it and then cache it
baseurl_data = cache_diction.get(BASEURL)
if not baseurl_data:
    baseurl_data = requests.get(BASEURL).text
    cache_data(CACHEFILE,BASEURL,cache_diction,baseurl_data)

# create a BeautifulSoup object with the data
soup = BeautifulSoup(baseurl_data, "html.parser")

# get the text of the class that contains the list of states in the dropdown and add each state to the database
dropdown =  soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
states_tags = dropdown.find_all('li')
for tag in states_tags:
    url = tag.a['href']
    split_url = url.split('/')
    new_state = State(State=tag.text,Abbr=split_url[2].upper(),URL='{}{}'.format(BASEURL,url))
    session.add(new_state)
session.commit()

# for each state, get the text from the url as stored in the db and cache it
states = session.query(State.Id,State.URL).all()
for state in states[0:5]:
    url = state[1]
    id = state[0]
    url_data = cache_diction.get(url)
    if not url_data:
        url_data = requests.get(url).text
        cache_data(CACHEFILE,url,cache_diction,url_data)
    soup = BeautifulSoup(url_data,'html.parser')
    parks_table = soup.find('ul', id='list_parks')
    parks_tags = parks_table.find_all('li',class_='clearfix')
    for tag in parks_tags:
        new_park = Park(Name=tag.h3.text,Type=tag.h2.text,Descr=tag.p.text.strip('\n'),Location=tag.h4.text,State=id)
        session.add(new_park)
    session.commit()