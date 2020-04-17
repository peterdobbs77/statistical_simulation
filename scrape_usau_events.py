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


def get_all_scoretables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table", class_="scores_table")


def get_scoretable_name(table):
    """Given a table soup, returns the table's name"""
    return table.find("thead").find("tr").find("th").text.strip()


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tbody").find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find("tbody").find_all("tr")[1:]:
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
# Shout out to https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python.


def scrape_and_clean_scoretables(base_url, event):
    # scrape
    soup = get_soup(base_url+event)
    tables = get_all_scoretables(soup)
    T = len(tables)
    print(f"Found {T} score tables")
    # clean
    frames = []
    for i, table in enumerate(tables, start=1):
        headers = get_table_headers(table)
        rows = get_table_rows(table)
        df = pd.DataFrame(rows, columns=headers)
        df['table'] = get_scoretable_name(table)
        df['event'] = event
        df['home_score'] = df['Score'].str.extract(r'(^\d+)').astype(int)
        df['away_score'] = df['Score'].str.extract(r'(\d+$)').astype(int)
        df = df[['event', 'table', 'Date', 'Time',
                 'Team 1', 'Team 2', 'home_score', 'away_score']]
        frames.append(df)
    result = pd.concat(frames)
    headers = ['event', 'table', 'Date', 'Time',
               'home_team', 'away_team', 'home_score', 'away_score']
    result.columns = headers
    return result


def scrape_and_clean_brackets(base_url, event):
    # scrape
    soup = get_soup(base_url+event)
    bracketgames = soup.find_all("div", {"class": "bracket_game"})
    print(f"Found {len(bracketgames)} bracket games")
    # clean
    games = []
    for i, game in enumerate(bracketgames):
        game_id = game['id']
        home_team = game.find(
            "span", {"class": "team", "data-type": "game-team-home"}).text
        away_team = game.find(
            "span", {"class": "team", "data-type": "game-team-away"}).text
        home_score = game.find(
            "span", {"class": "score", "data-type": "game-score-home"}).text
        if home_score == "F" or home_score == "W" or home_score == "L":
            home_score = 0
        else:
            home_score = int(home_score)
        away_score = game.find(
            "span", {"class": "score", "data-type": "game-score-away"}).text
        if away_score == "F" or away_score == "W":
            away_score = 0
        else:
            away_score = int(away_score)
        game_time = game.find("span", {"class": "date"}).text
        games.append([event, game_id, game_time, home_team,
                      away_team, home_score, away_score])
    headers = ['event', 'game_id', 'game_time', 'home_team',
               'away_team', 'home_score', 'away_score']
    result = pd.DataFrame(games, columns=headers)
    return result


BASE_URL = "https://play.usaultimate.org/events/"
# TODO: update this for each event
EVENT = "Meltdown-2017/schedule/Men/CollegeMen/"
FILE_PATH = f"./data/ultimate/{EVENT}"

if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

print(f"Data files will be stored under {FILE_PATH}")

# scrape pool play games
poolplay = scrape_and_clean_scoretables(BASE_URL, EVENT)
poolplay.to_csv(f"{FILE_PATH}poolplay.csv")

# scrape bracket play games
bracketplay = scrape_and_clean_brackets(BASE_URL, EVENT)
bracketplay.to_csv(f"{FILE_PATH}bracketplay.csv")

# combine all games and indicate winners and losers
poolplay['type'] = "pool"
bracketplay['type'] = "bracket"
all_games = poolplay[['event', 'type', 'home_team', 'away_team', 'home_score', 'away_score']].append(
    bracketplay[['event', 'type', 'home_team', 'away_team', 'home_score', 'away_score']], ignore_index=True)
home = all_games[all_games['home_score'] > all_games['away_score']]
home.columns = ['event', 'type', 'winner_team',
                'winner_score', 'loser_team', 'loser_score']
away = all_games[all_games['home_score'] < all_games['away_score']]
away.columns = ['event', 'type', 'loser_team',
                'loser_score', 'winner_team', 'winner_score']
reorganized = home.append(away, ignore_index=True, sort=False)
reorganized.to_csv(f"{FILE_PATH}all_games.csv")
