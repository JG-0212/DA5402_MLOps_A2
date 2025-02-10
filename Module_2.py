from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

class WebDriverInitializationError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class BrowserAccessError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass


def top_stories_scrape(url):
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
    browser.quit()

    if ps is None:
        raise GoogleNewsRetrievalError 
    else:
        return ps