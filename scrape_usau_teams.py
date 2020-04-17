import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"


def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")


def scrape_and_clean_scheduletables(base_url, event):
    # scrape
    soup = get_soup(base_url+event)
    schedule_table = soup.find("table", {"class": "schedule_table"})


BASE_URL = "https://play.usaultimate.org/events/"
# TODO: update this for each event
EVENT = "Meltdown-2017/schedule/Men/CollegeMen/"
FILE_PATH = f"./data/ultimate/{EVENT}"

if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

print(f"Data files will be stored under {FILE_PATH}")

# scrape pool play games
teamplay = scrape_and_clean_scheduletables(BASE_URL, EVENT)
teamplay.to_csv(f"{FILE_PATH}teamplay.csv")
