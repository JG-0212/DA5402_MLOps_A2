import configparser
from urllib.parse import urljoin,urlencode
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
from bs4 import BeautifulSoup

class WebDriverInitializationError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class BrowserAccessError(Exception):
    """Exception raised when unable to access the Browser."""
    pass

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class ClasschangeError(Exception):
    """Exception raised when Top Stories class change."""
    pass

def get_home_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_url = config['GoogleNews']['base_url']
    home_ep = config['GoogleNews']['home_endpoint']
    params = {
        'hl': config['GoogleNews']['language'],
        'gl': config['GoogleNews']['country'],
        'ceid': config['GoogleNews']['client_id']
    }

    return f"{urljoin(base_url,home_ep)}?{urlencode(params)}"

def m1():
    url = get_home_url()

    options = Options()
    options.add_argument('--headless')
    try:
        browser = webdriver.Edge(options=options)  
    except WebDriverInitializationError as e:
        raise e

    try:      
        browser.get(url)
    except BrowserAccessError as e:
        raise e
    
    time.sleep(2)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    ps = browser.page_source
    if ps is None:
        raise GoogleNewsRetrievalError 
    
    browser.quit()

    soup = BeautifulSoup(ps, "html.parser")
    top_stories_link = soup.find('a',class_ = 'aqvwYd')
    if top_stories_link:
        url_ts = top_stories_link['href']
        return [urljoin(url,url_ts)]
    else:
        raise ClasschangeError

if __name__ == '__main__':
    m1()
