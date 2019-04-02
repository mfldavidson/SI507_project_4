# SI 507 Project 4 Option 1: Scraping the NPS Website to Create a CSV of National Parks
##### Maggie Davidson, jmaggie

## About the Program
This program in SI507_project_4.py scrapes the National Park Service website using the BeautifulSoup library, caches the data returned from each endpoint, creates a database with the returned data, and writes the data into a CSV file of each National Park. The program uses a SQLite database defined in setup.py (by importing setup.py into SI507_project_4.py) and caching functions defined in caching.py.

### About setup.py
setup.py creates a SQLite database 'state_parks.sqlite' and 3 tables:
- States table with attributes Id, State (full name of the state/territory), Abbr (2-character state/territory abbreviation), URL (the URL of the page on the NPS website for this state's National Parks as pulled from 'https://www.nps.gov')
- Parks table with attributes Id, Name, Type, Descr (brief description blurb of the park), Location (text description of the park's location)
- Association table with attributes Park_Id and State_Id to create a many-to-many relationship between the States table and Parks table

### About caching.py
caching.py defines two functions:
- open_cache, which takes one input, the name of the cache file, and attempts to open it and read the contents into a dictionary; if that fails, it creates an empty dictionary; the function returns the dictionary
- cache_data, which takes 4 inputs: the name of the cache file, a string representing the url the data came from, the cache dictionary, and the new data to be added to the cache file; the function adds the new data to the cache dictionary with the key as the url string and the value as the new data, then saves the cache dictionary into the cache file

# How to Run the Program
This program was written with Python Anaconda, BeautifulSoup (bs4), requests, and SQLAlchemy using a virtual environment. Requirements to run the program can be found in requirements.txt. To install everything from requirements.txt, download the requirements.txt file, activate your virtual environment, and then enter the following in your shell: `pip install -r requirements.txt`.

In order to run the program, make sure you are in the same directory as all the files, and then enter the following in your shell: `python SI507_project_4.py`. The program will create or update the following files:
- nps_cache.json, a cache file of all the data retrieved from the internet
- state_parks.sqlite, a SQLite database of all the states and parks
- nps_parks.csv, a CSV file of all of the National Parks
