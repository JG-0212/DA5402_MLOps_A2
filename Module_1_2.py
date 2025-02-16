import configparser
from urllib.parse import urljoin,urlencode
import requests
import time
from bs4 import BeautifulSoup
import importlib
import os

#Defining a few exceptions useful for the program
class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class ClasschangeError(Exception):
    """Exception raised when Top Stories class change."""
    pass

#Function to retriev home url and top stories HTML class from  configuration file
def get_home_url_top_stories_class():
    config = configparser.ConfigParser()
    config.read('dags/assignment-02-JG-0212/a2_config.ini')

    print("Succesfully read config file")
    for section in config.sections():
    	print(f"[{section}]")
    print("No sections found")
    base_url = config['GoogleNews']['base_url']
    home_ep = config['GoogleNews']['home_endpoint']
    params = {
        'hl': config['GoogleNews']['language'],
        'gl': config['GoogleNews']['country'],
        'ceid': config['GoogleNews']['client_id']
    }
    ts_class = config['GoogleNews']['top_stories_class']

    return f"{urljoin(base_url,home_ep)}?{urlencode(params)}",ts_class

#Function to scrape top stories page and return its URL and the Top Stories Page source
def top_stories_scrape():
    url,ts_class = get_home_url_top_stories_class()
    ps = requests.get(url)
    if ps is None:
        print("Error in retrieving home page")
        raise GoogleNewsRetrievalError 
    print("Home page succesfully retrieved")
    soup = BeautifulSoup(ps.text, "html.parser")
    top_stories_link = soup.find('a',class_ = ts_class)
    if top_stories_link:
        print("Top stories page succesfully retrieved")
        url_ts = top_stories_link['href']
        abs_url_ts = urljoin(url,url_ts)
        ts_ps = requests.get(abs_url_ts).text
        return [abs_url_ts,ts_ps]
    else:
        raise ClasschangeError
