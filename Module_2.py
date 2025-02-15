import time

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

def pull_ts_url(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='return_value', task_ids='base_scrape')
    return pulled_value_1

def top_stories_scrape(**kwargs):

    url = pull_ts_url(**kwargs)
    ps = browser.page_source
    browser.quit()

    if ps is None:
        raise GoogleNewsRetrievalError 
    else:
        return ps