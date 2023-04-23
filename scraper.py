from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

teams_dict = {
    "maccabi-haifa": str(1064),
    "maccabi-tel-aviv": str(119)
}


def scrape_team_by_year(team, year):
    url = "https://www.transfermarkt.com/" + team + "/kader/verein/" + teams_dict[team] + "/saison_id/" + str(year)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = []
    for class_name in ["odd", "even"]:
        html_text = soup.find_all(class_=class_name)
        for snippet in html_text:
            player_name = re.search(r'alt="(.*?)" class="bilderrahmen', str(snippet)).group(1)
            players.append(player_name)

    df = pd.DataFrame(players, columns=['name'])
    df[year] = team
    return df


def scrape_team(team):
    years = [i for i in range(2013,2023)]
    df = scrape_team_by_year(team, 2012)
    for year in years:
        temp = scrape_team_by_year(team, year)
        df = pd.merge(df, temp, on='name', how='outer')

    return df


def combine_years(df):
    # Define the pattern of column names to merge and combine
    column_pattern = '{}_{}'

    # Define the start and end years of the columns to merge and combine
    start_year = 2012
    end_year = 2022

    # Loop over the range of years to merge and combine
    for year in range(start_year, end_year + 1):
        col_name_x = column_pattern.format(year, 'x')
        col_name_y = column_pattern.format(year, 'y')
        col_name = str(year)

        df[col_name] = df[col_name_x].fillna(df[col_name_y])
        df = df.drop(columns=[col_name_x, col_name_y])

    return df

