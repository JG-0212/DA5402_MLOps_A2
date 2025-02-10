import requests
from bs4 import BeautifulSoup
import configparser
from urllib.parse import urljoin,urlencode,urlparse
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pytz
import os
import psycopg2
from config import config
import base64
import requests

def get_image_base64_from_url(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    base64_encoded_image = base64.b64encode(response.content).decode('utf-8')
    return base64_encoded_image


def is_relative_url(url):
    parsed_url = urlparse(url)
    return not parsed_url.scheme 


def extract_data(url,ps):
    soup = BeautifulSoup(ps, "html.parser")
    images = soup.find_all('img')
    
    thumbnails = []
    headlines = []

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


    