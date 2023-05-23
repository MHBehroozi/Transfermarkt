# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: env_bootcamp_conda
#     language: python
#     name: python3
# ---

# # import libraries

import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import re
import numpy as np
import time
import jupytext


# # Extracting all leagues titles and urls

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           "Accept-Language": "en-US,en;q=0.5"}

Countries_Name = ['England', 'Germany', 'Italy', 'France', 'Spain']
Countries_1stLeagueName = ['premier-league', 'bundesliga', 'serie-a', 'ligue-1', 'laliga']
Countries_Url = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=20',
             'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=20',
             'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1/plus/?saison_id=20',
             'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=20',
             'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1']

# # Request all leagues pages and extract clubs urls and titles

# +
links = []
titles = []
countries = []

for i, url in enumerate(Countries_Url):
    country = Countries_Name[i]
    for i in range(15,22):
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='responsive-table')

        if table:
            rows = table.find_all('td', class_='hauptlink no-border-links')

            for row in rows:
                team_link = row.find('a')
                
                if team_link:
                    team_href = team_link.get('href')
                    team_title = team_link.get('title')
                    if team_title not in titles:
                        links.append(team_href)
                        titles.append(team_title)
                        countries.append(country)
                        
        time.sleep(random.random())
# -

print(len(dict(zip(titles,links))))
print('*'*50)
dict(zip(titles,links))

ids = [re.search(r'verein/(.*?)/saison_id', element).group(1) for element in links]
link_titles = [re.search(r'(.*?)/startseite', element).group(1) for element in links]

# # Generating cup pages for every club

# +
main_url = 'https://www.transfermarkt.com'
extension = '/erfolge/verein/'

Victories_page_links = []

for i in range(len(links)):
    page_link = main_url + link_titles[i] + extension + ids[i]
    Victories_page_links.append(page_link)
# -

Victories_page_links

len(Victories_page_links)

# # Request every cup page

# +
soups = []

for url in Victories_page_links:
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    soups.append(soup)
    time.sleep(random.random())
# -

# # Extracting cup tags for each club

cup_tags = []
for soup in soups:
    cup_tags.append(soup.select('div.large-6.columns div.box'))


# transforming '16/17' to '2016'
def year_transformer(raw_year):
    year = raw_year.split('/')[0]
    if len(year) == 2:
        if int(year) <=22:
            return '20' + year
        else:
            return '19' + year
    elif len(year) == 4:
        return year


# # Find all cups for each cup page and club from cup_tags

# +
result = []
for i, club_tag in enumerate(cup_tags):
    country = countries[i]
    club_name = titles[i]
    club_id = ids[i]
    for tag in club_tag:
        cup_name = tag.find('img').get('title')
        years_part = tag.find('div', class_='erfolg_infotext_box').get_text()
        years = [year_transformer(element) for element in years_part.split() if not element.__contains__(',')]
        for year in years:
            year = int(year)
            result.append({'nation': country, 'club_id':club_id, 'club_name':club_name, 'cup_name':cup_name, 'win_year_from':year, 'win_year_to':year+1})
    

# -

# # Convert and export results

df = pd.DataFrame(result)
df.to_csv('cup_winners.csv', index=False)

df_selection = df[(df.win_year_from >=2015) & (df.win_year_to<=2022)].reset_index(drop=True)
df_selection

df_selection.to_csv('cup_winners_selected.csv', index=False)

# !jupytext --to py -o cup_crawler.py cup_crawler.ipynb
