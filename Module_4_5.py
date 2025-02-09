import requests
from bs4 import BeautifulSoup
import configparser
from urllib.parse import urljoin,urlencode,urlparse
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
import pytz
import os
import psycopg2
from config import config

class WebDriverInitializationError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class BrowserAccessError(Exception):
    """Exception raised when unable to initialize the WebDriver."""
    pass

class GoogleNewsRetrievalError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass

class SQLConnectionError(Exception):
    """Exception raised when unable to retrieve Google News content."""
    pass


def download_image(url, id, folder='thumbnails'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = str(id)
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully: {filepath}")
        return filepath
    else:
        print("Failed to download image")
        return -1

def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1

def insert_1(conn,data):
    cur = conn.cursor()
    sql =  """
    INSERT INTO image_data (headline, thumbnail_location, store_id)
    VALUES (%s, %s, %s);
    """
    cur.execute(sql,data)
    conn.commit()

def insert_2(conn,data):
    cur = conn.cursor()
    sql =  """
    INSERT INTO article_metadata (headline, scrape_timestamp, article_date, store_id)
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql,data)
    conn.commit()

def headline_exists(cursor,headline):
    query = "SELECT EXISTS(SELECT 1 FROM image_data WHERE headline = %s);"
    cursor.execute(query, (headline,))
    result = cursor.fetchone()[0]
    return bool(result)

def main(thumbnails,headlines):

    ist_timezone = pytz.timezone('Asia/Calcutta')
    current_timestamp = datetime.now(ist_timezone)
    formatted_timestamp = current_timestamp.isoformat()
    article_date = current_timestamp.date().isoformat()

    conn = connect()

    if conn == -1:
        raise SQLConnectionError
    sql = '''
        SELECT store_id
        FROM image_data
        ORDER BY store_id DESC
        LIMIT 1;
        '''
    obj = conn.cursor().execute(sql)
    if obj is None:
        id = 0
    else:
        id = obj.fetchone()

    for t,h in zip(thumbnails,headlines):

        if headline_exists(conn.cursor(),h):
            continue


        filepath = download_image(t,id)

        if filepath == -1:
            continue
        insert_1(conn,(h,filepath,id))
        insert_2(conn,(h,formatted_timestamp,article_date,id))
        id += 1



