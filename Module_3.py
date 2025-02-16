import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import base64
import requests

#Function to get the base64 encoded version of an image from its absolute URL
def get_image_base64_from_url(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    base64_encoded_image = base64.b64encode(response.content).decode('UTF-8')
    return base64_encoded_image

#Function to check whether an URL is relative (logic for identifying the thumbnail images)
def is_relative_url(url):
    parsed_url = urlparse(url)
    return not parsed_url.scheme 

#Function for pulling returned values from kwargs using x_com
def pull_ts_scrape(**kwargs):
    ti = kwargs['ti']
    pulled_value_1 = ti.xcom_pull(key='return_value', task_ids='ts_scrape')
    return pulled_value_1

#Function to extract thumbnails and headlines from the Top Stories page source
def extract_data(**kwargs):
    url,ps = pull_ts_scrape(**kwargs)
    soup = BeautifulSoup(ps, "html.parser")
    images = soup.find_all('img')
    
    thumbnails = []
    headlines = []
    #The headline is identified as the text immediately after or before the thumbnail which is identified
    # by soup and its relative URL as an API attachment
    for img in images:
        next_a = img.find_next('a')
        prev_a = img.find_previous('a')
        if is_relative_url(img['src']) and ((next_a and next_a.text) or (prev_a and prev_a.text)):
            img_url = requests.compat.urljoin(url, img['src'])
            thumbnail = get_image_base64_from_url(img_url)
            if next_a and next_a.text:
                headline = next_a.text
            else:
                headline = prev_a.text 

            thumbnails.append(thumbnail)
            headlines.append(headline)
    
    return [thumbnails,headlines]


    
