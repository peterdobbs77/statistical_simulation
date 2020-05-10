import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

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


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows


BASE_URL = "https://www.usaultimate.org/news/college-rankings-open-apr-3-2013/"
# scrape
soup = get_soup(BASE_URL)
table = soup.find("div", {"id": 'rules_list'}).find("table")
# clean
rows = get_table_rows(table)
df = pd.DataFrame(rows[1:], columns=rows[0])
df['W'] = df['W - L'].str.extract(r'(^\d+)')
df['L'] = df['W - L'].str.extract(r'(\d+$)')
df['season'] = '2013_college'
df = df[['season', 'Rank', 'Team', 'PR', 'Region', 'Conf', 'W', 'L']]
df.to_csv(f'./data/ultimate/archives/open_2013_college_rankings.csv', index=False)
