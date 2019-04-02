from bs4 import BeautifulSoup
import requests, json, csv
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

# get the text of the class that contains the list of states in the dropdown and add each state to the database if it doesn't already exist
dropdown =  soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
states_tags = dropdown.find_all('li')
for tag in states_tags:
    # get the url to retrieve the state abbreviation and check if the state is already in the db
    url = tag.a['href']
    split_url = url.split('/')
    state_exists = session.query(State.Abbr).filter(State.Abbr.like(split_url[2])).all()
    # if the state doesn't already exist, add it to the db
    if not state_exists:
        new_state = State(State=tag.text,Abbr=split_url[2].upper(),URL='{}{}'.format(BASEURL,url))
        session.add(new_state)
session.commit()

# for each state retrieved from the States table, get the text from the url as stored in the db, cache it, and create a BeautifulSoup object
states = session.query(State.Id,State.URL).all()
for state in states:
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
        # check if the park already exists in the db
        park_exists = session.query(Park).filter(Park.Name == tag.h3.text).all()
        # if park exists, create a new relationship; if the park doesn't already exist, add it to the db
        if park_exists:
            rel_exists = session.query(StateParkAssociation).filter(StateParkAssociation.Park_Id == park_exists[0].Id, StateParkAssociation.State_Id == id).all()
            if rel_exists:
                break
            else:
                new_rel = StateParkAssociation(State_Id=id,Park_Id=park_exists[0].Id)
                session.add(new_rel)
                session.commit()
        else:
            new_park = Park(Name=tag.h3.text,Type=tag.h2.text,Descr=tag.p.text.strip('\n'),Location=tag.h4.text)
            session.add(new_park)
            session.commit()
            new_rel = StateParkAssociation(State_Id=id,Park_Id=new_park.Id)
            session.add(new_rel)
    session.commit()

# write the data to a csv
with open('nps_parks.csv','w') as parks_file:
    parkwriter = csv.writer(parks_file)
    parkwriter.writerow(['Park Name','Park Type','Park Location Description','Park Description','Park States'])
    parks = session.query(Park).all()
    for park in parks:
        states = []
        rels = session.query(StateParkAssociation).filter(StateParkAssociation.Park_Id == park.Id).all()
        for rel in rels:
            new_state = session.query(State).filter(State.Id == rel.State_Id).first()
            states.append(new_state.Abbr)
        parkwriter.writerow([park.Name,park.Type,park.Location,park.Descr,', '.join(states)])
