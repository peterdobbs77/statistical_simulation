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


def get_table_headers(table):
    """Given a statistics table soup, returns all the headers"""
    headers = []
    for th in table.find("thead").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find("tbody").find_all("tr"):
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


def scrape_and_clean_archive_tables_pre2014(base_url, arch_id):
    """valid for retrieving archive tables from 1989 - 2013"""
    # scrape
    soup = get_soup(base_url+arch_id)
    tables = soup.find_all("table", class_="tablesorter")
    # table index = -2 for 1989 - 2014, index = -1 before that
    open_final_rankings = tables[-2]
    # clean
    headers = get_table_headers(open_final_rankings)
    rows = get_table_rows(open_final_rankings)
    df = pd.DataFrame(rows, columns=headers)
    return df


BASE_URL = "https://www.usaultimate.org/archives/"
for year in range(1989, 2013):
    ARCH_ID = f"{year}_college"
    archive_table = scrape_and_clean_archive_tables_pre2014(
        BASE_URL, f"{ARCH_ID}.aspx")
    archive_table["season"] = ARCH_ID
    archive_table.to_csv(
        f'./data/ultimate/archives/open_{ARCH_ID}_scraped.csv', index=False)

# combine data


def flatten(listoflists): return [
    item for sublist in listoflists for item in sublist]


data_rows = []
for year in range(1989, 2013):
    data_file = f'./data/ultimate/archives/open_{year}_college_scraped.csv'
    temp_df = pd.read_csv(data_file)
    temp_df = temp_df[
        ['season', 'Rank', 'Team', 'PR', 'W', 'L', 'Win %']]
    data_rows.append(temp_df.values.tolist())


df = pd.DataFrame(flatten(data_rows), columns=[
                  'season', 'Rank', 'Team', 'PR', 'W', 'L', 'Win %'])
df.to_csv(f'./data/ultimate/archives/open_college_archive_scraped.csv', index=False)
