import streamlit as st


st.set_page_config(
    page_title='Transfermarkt',
    page_icon= ':soccer:'
)
st.title("Part 1: Data Gathering and Web Scraping")

st.header('General View')

'According to the request of the project and the need for information for the analysis of next parts, in first part of project we have crawled [transfermarkt.com](transfermarkt.com).'
'The data listed below were crawled. Related Jupiter notebooks are linked for each section.:'
'* [5 Top League Clubs and their Statistics](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/League_crawl)'
'* [Market Balance and Transfers for Clubs](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/Club_transfers_crawl)'
'* [Players General Details, Statistics and Transfers](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/Player_crawl)'
'* [Awards and Cups that each Club has earned](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/Cup_crawl)'

"Also other Data has Crawled, for all of them, Codes and Jupyter Notebooks are in the Project's [GitHub Repository](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data)."

"---------"

st.header('Tools and Libraries')
'''
For downloading web pages, `requests` library has been used, We requested web page by `requests.get()` and parse recieved pages using `BeautifulSoup` python library.
You can see our code shape like this:
'''
st.code("""
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
""",
        language="python")

"It should be noted that during crawling, we encountered many problems, which can be said to be mostly due to the bad state of the country's internet. In many cases, proxies and VPNs were used."

'In [transfermarkt.com](transfermarkt.com), each League, Club and Player have a unique **ID** and all URL address for their web pages have a pattern that can be changed based on these **IDs**. Based on this pattern, we have been able to crawl a lot of data.'

'In each section, we used `pandas.DataFrame` to make tables of crawled records and save them as CSVs. In the following, we will examine a part of the code for each section:'
"---------"

st.header('Crawling League Clubs and their Statistics')

"""
In this section, we'd need to get folowing information for each Club in 5 top Leagues of England, France, Italy, Germany and Spain for seasons during 2015/16 to 2021/22:
* Club Name
* League name
* Average age of players
* Stadium name
* Coach name
* Coach Date
* Club Values

For example, in the following, you can see code used for crawling Laliga (Spain premier league soccer). Also final Laliga CSV can be checked in this [Link](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/League_crawl/Laliga).
"""

st.code("""
def get_Laliga_teams(url):

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', class_='responsive-table')

    teams = []
    if table:
        rows = table.find_all('td')
        
        for row in rows:
            team_link = row.find('a')
            
            if team_link:
                team_href = team_link.get('href')
                if team_href not in teams and 'startseite'in team_href:
                   teams.append(team_href)
                   href_name.append(team_href.split("/")[1])   
    return teams
""",
    language="python")

st.code("""
for id_year in ['2021','2020','2019','2018','2017','2016','2015']:
    club_values=[]
    coach=[]
    coach_date=[]
    href_name=[]
    data_dict=[]
    club_name=[]
    stadium_name=[]
    league_name=[]
    avg_players=[]

    url=f'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id={id_year}'
    premier_league_teams = get_Laliga_teams(url)
    premier_league_teams=list(dict.fromkeys(premier_league_teams))
    for href in premier_league_teams:
        club,league,avg_player,stadium=team_link(href)
        club_name.append(club)
        league_name.append(league)
        avg_players.append(avg_player)
        stadium_name.append(stadium)
        data_dict.append(
       {
        'Club Name':club_name.pop(),
        'League name':league_name.pop(),
        'Average age of players':avg_players.pop(),
        'Stadium name':stadium_name.pop(),
        'Coach name':coach.pop(),
        'Coach Date':coach_date.pop(),
        'Club Values': club_values.pop(),
       }
       ) 
    df = pd.DataFrame(data_dict,columns=['Club Name',
        'League name',
        'Average age of players',
        'Stadium name',
        'Coach name',
        'Coach Date',
        'Club Values'])
    df.to_csv(f'laliga_{id_year}.csv') 
""",
    language="python")

"---------"

st.header('Market Balance and Transfers for Clubs')
"""
In this section we have crawled data of Income and Expenditure that each Club has made in each season. Crawled data can be checked in this [Link](https://github.com/MHBehoozi/Transfermarkt/blob/master/WebScraping_data/Club_transfers_crawl/over_all_balance.csv) and it cointains following deitails for each club:
* Club ID
* Club Country
* Link for Club
* Season
* Total Income and Expenditure for each Season
* Total Player number that Join or Left the Club

In the following, you can see part of code used to extract mentioned Data:
"""

st.code("""
country_url={'England':' https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
             'Spain' : 'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
             'Italy':   'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
             'Germany':'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1',
             'France': 'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1'}
""",
    language="python")

st.code("""
links=[]
clubs=[]
ids=[]
countries=[]
seasons=[]
income_arrivals=[]
incomes=[]
overall_balance=[]
expend_arrivals=[]
expends=[]
years=np.arange(2015,2022) 

for country, url in country_url.items():
    for year in years:
        s_url=url +'/plus/?saison_id='+ str(year) 
        main_page= requests.get(s_url,headers=headers)
        soup = BeautifulSoup(main_page.content, 'html.parser')
        table=soup.find('table',attrs={'class':'items'})
        trs=table.find_all('tr') 
        for tr in trs[2:]:
            td=tr.find('td',attrs={'class':'hauptlink no-border-links'}).find('a', href=True) 
            link='https://www.transfermarkt.com'+ td['href']
            name=td['title'] 
            id=link.split('https://www.transfermarkt.com/')[1].split('/')[3] 
            clubs.append(name)
            ids.append(id) 
            countries.append(country)
            links.append(link)
          
            seasons.append(year)
            #tranfer table 
            page=requests.get(link,headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser') 
            transfer_record_box=soup.find_all('div', attrs={'data-viewport':'Transferbilanz'})[0] 
            income_td=transfer_record_box.find('table').find('tbody').find('tr',attrs={'class':'transfer-record__revenue'})
            income_arrival=income_td.find('td',attrs={'class':'zentriert test-class transfer-record__text'}).text
            income_arrivals.append(income_arrival)

            income=income_td.find('td',attrs={'class':'transfer-record__total transfer-record__total--positive'}).text.split('\n')[1].rstrip().lstrip()
            incomes.append(income) 

            expend_td=transfer_record_box.find('table').find('tbody').find('tr',attrs={'class':'transfer-record__expenses'})
            expend_arrival=expend_td.find('td',attrs={'class':'zentriert transfer-record__text'}).text 
            expend_arrivals.append(expend_arrival)

            expend=expend_td.find('td',attrs={'class':'transfer-record__total transfer-record__total--negative'}).text.split('\n')[1]
            expends.append(expend)
            try:
                overall_td=transfer_record_box.find('table').find('tfoot').find('tr').find('td',attrs={'class':'redtext rechts transfer-record__total'}).text.replace('\n','')
            except:
                try:
                    overall_td=transfer_record_box.find('table').find('tfoot').find('tr').find('td',attrs={'greentext rechts transfer-record__total'}).text.rstrip().lstrip()
                except:
                    overall_td=transfer_record_box.find('table').find('tfoot').find('tr').find('td',attrs={'rechts transfer-record__total'}).text.rstrip().lstrip().replace('+','')
 
            overall_balance.append(overall_td)           
""",
    language="python")

st.code("""
clubs_id={}
clubs_id['Club']=clubs
clubs_id['id']=ids
clubs_id['Country']=countries
clubs_id['link']=links
clubs_id['Season']=seasons
clubs_id['income']=incomes 
clubs_id['expend']=expends
clubs_id['overall_balance']=overall_balance
clubs_id['income_arrival']=income_arrivals
clubs_id['expend_arrival']=expend_arrivals

df=pd.DataFrame(data=clubs_id) 
df.to_csv('over_all_balance.csv', index=False)
""",
    language="python")

"---------"

st.header('Players Data Crawling')
"""
Players Data has Crawled using a main code block and functions for each detailed. in the following, you can see main code block and for checking all functions you can open this section [Jupyter Notebook](https://github.com/MHBehoozi/Transfermarkt/blob/master/WebScraping_data/Player_crawl/Data_collection_of_soccer_players.ipynb). Also you can crawled CSVs in this [Link](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/Player_crawl/player%20info%20csvs)
"""

st.code("""
country_season_link_format = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}/saison_id/{}/plus/1'
country_id = {'189', '50', '157', '40', '75'} #England, France, Spain, Germany, Italy
#country_id = {'189'} #England, France
season = {'2021', '2020', '2019', '2018', '2017', '2016', '2015'}

#link variables
all_season_leagues=[]
all_league_teams={}
all_team_players={}

#test variables
player_ids=[]
player_count=0

#final tables culomns & Each player's table
player_table_culomns = ['player_id', 'name', 'birth_date', 'height', 'current_international', 'main_position', 'foot', 'current_club', 'goals_scored', 'goals_assisted', 'goals_conceded', 'clean_sheets', 'total_appearence', 'agent']
transfer_table_culomns = ['player_id', 'Season', 'Date', 'Left', 'Joined', 'MV', 'Fee']

player = pd.DataFrame(columns = player_table_culomns)
transfer = pd.DataFrame(columns = transfer_table_culomns)
statistics = pd.DataFrame()

#final tables (all datas from players)
player_table = pd.DataFrame(columns = player_table_culomns)
transfer_table = pd.DataFrame(columns = transfer_table_culomns)
statistics_table = pd.DataFrame()


for c_id in tqdm(country_id, desc ="countries"):
  
  for i, s_id in enumerate(season):
    link = country_season_link_format.format(c_id, s_id)
    
    all_season_leagues=(league_links(link))
    #print('----- leagues links',all_season_leagues)
    
    for league_link in tqdm(all_season_leagues, desc='leagues'):
      #print(league_link)
      all_league_teams=(team_links(league_link))
      
      for team_link in tqdm(all_league_teams, desc='teams'):  
       
        all_team_players=(player_links(team_link))
        for player_link in (all_team_players):
        
          try:
            if player_id(player_link) not in player_ids:
              player_count+=1
              #print ('new id added','   ',player_count,'  ', player_id(player_link))
              player_ids.append(player_id(player_link))
              #player, transfer = find_player_info(player_link)
              player, transfer, statistics = find_player_info(player_link)
              
              player_table.loc[len(player_table.index)]= player
              transfer_table = pd.concat([transfer_table, transfer], axis=0,  ignore_index = True)
              statistics_table = pd.concat([statistics_table, statistics], axis=0,  ignore_index = True)

            else:
              print(player_link + ' duplicate id found and skiped')
            continue
          except:
            print(player_link + ' something wrong and skiped')           
            continue
          


player_table.to_csv('player_table.csv', encoding='utf-8')
transfer_table.to_csv('trasnfer_table.csv', encoding='utf-8')
statistics_table.to_csv('statistics_table.csv', encoding='utf-8')
""",
    language="python")

"---------"

st.header('Awards and Cups')

"""
Each Club has a Awards and Cups web page, after requesting thest web pages, we extract cups that each Club has earned in each season using following code. You can check crawled data CSV in this [Link](https://github.com/MHBehoozi/Transfermarkt/blob/master/WebScraping_data/Cup_crawl/cup_winners_selected.csv).
"""

st.code("""
cup_tags = []
for soup in soups:
    cup_tags.append(soup.select('div.large-6.columns div.box'))

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

df = pd.DataFrame(result)
df_selection = df[(df.win_year_from >=2015) & (df.win_year_to<=2022)].reset_index(drop=True)
df_selection.to_csv('cup_winners_selected.csv', index=False)
""",
    language="python")