import configparser
from urllib.parse import urljoin,urlencode
import requests
import time
from bs4 import BeautifulSoup
import importlib
import os

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class ClasschangeError(Exception):
    """Exception raised when Top Stories class change."""
    pass

def get_home_url():
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

    return f"{urljoin(base_url,home_ep)}?{urlencode(params)}"

def top_stories_scrape():
    url = get_home_url()
    ps = requests.get(url)
    if ps is None:
        print("Error in retrieving home page")
        raise GoogleNewsRetrievalError 
    print("Home page succesfully retrieved")
    soup = BeautifulSoup(ps.text, "html.parser")
    top_stories_link = soup.find('a',class_ = 'aqvwYd')
    if top_stories_link:
        url_ts = top_stories_link['href']
        abs_url_ts = urljoin(url,url_ts)
        ts_ps = requests.get(abs_url_ts).text
        print("Is abs_url_ts none")
        print(abs_url_ts is None)
        print("Is ts_ps None")
        print(ts_ps is None)
        return [abs_url_ts,ts_ps]
    else:
        raise ClasschangeError
