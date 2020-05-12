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


def scrape_and_clean_archive_tables(base_url, dataset_id):
    """valid for retrieving archive tables after 2012"""
    # scrape
    soup = get_soup(base_url+dataset_id)
    table = soup.find("table", class_="global_table")
    # clean
    rows = get_table_rows(table)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


BASE_URL = "https://play.usaultimate.org/teams/events/team_rankings/?DataSetId="
DATASETID = f"D97nl6Hr63Ip0qKyPyFqnf%2bCzVCqonUm8mMti7DMikA%3d"
SEASON = '2016_college'
rankings = scrape_and_clean_archive_tables(BASE_URL, DATASETID)
rankings['dataset_id'] = DATASETID
rankings['season'] = SEASON
rankings.to_csv(
    f'./data/ultimate/archives/open_{SEASON}_rankings.csv', index=False)
