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


def is_relative_url(url):
    parsed_url = urlparse(url)
    return not parsed_url.scheme 


def main(url,ps):
    soup = BeautifulSoup(ps, "html.parser")
    images = soup.find_all('img')
    
    thumbnails = []
    headlines = []

    for img in images:
        next_a = img.find_next('a')
        prev_a = img.find_previous('a')
        if is_relative_url(img['src']) and ((next_a and next_a.text) or (prev_a and prev_a.text)):
            img_url = requests.compat.urljoin(url, img['src'])

            if next_a and next_a.text:
                headline = next_a.text
            else:
                headline = prev_a.text 

            thumbnails.append(img_url)
            headlines.append(headline)
    
    return [thumbnails,headlines]


    