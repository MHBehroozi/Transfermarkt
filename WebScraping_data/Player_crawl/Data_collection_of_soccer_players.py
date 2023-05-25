# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# + [markdown] id="8WYCFcT-KZ4O"
# # Data collection of soccer players

# + [markdown] id="fg_NZPKpKf9w"
# ## Libraries

# + id="hYlatFBiKjDZ"
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
#from tqdm import tqdm
from tqdm.notebook import trange, tqdm
import time 
import csv
import re


# + [markdown] id="npjTGAldZyXF"
# ##Functions

# + [markdown] id="dmKErzN8L27m"
# ### id

# + id="r8F6gMeRL4nd"
def player_id(link):
  try:
    player_id = (str(link).split('/'))[-1]
    return player_id
  except:
    print(link+" player id not found!")
    return np.nan


# + [markdown] id="VIVowCYuYITG"
# ### name and lastname

# + id="8Vai1ld3YMgu"
def player_name (page_content,link):
  try:
    #get the name tag
    full_name = page_content.find('h1',class_='data-header__headline-wrapper').get_text()
    #Remove extra space
    full_name = (" ".join(full_name.strip().split()))
    #Separating name and last name
    full_name = re.sub(r'#\d+','', full_name).strip()
    name = full_name.split(' ')[0]
    last_name = full_name.split(' ')[-1]

    return full_name
    #return name, last_name
    #print(full_name,'\n'+name ,'\n'+last_name)
  
  except:
    print(link+" player name not found!")
    return np.nan


# + [markdown] id="xhrKjIv8bPPi"
# ### Place of birth

# + id="JVjeb6GwbSJS"
def place_of_birth(page_content, link):
  try:
    place_of_birth = page_content.find(['span'], string=['Place of birth:']).find_next('img')['title']
    return place_of_birth

  except:
    print(link+" player place of birth not found!")
    return np.nan


# + [markdown] id="szIeZu7_YUSH"
# ### Date of birth (age)

# + id="Vt7y5knzYT33"
# date of birth
def date_of_birth(page_content, link):
  try:
    date_of_birth = page_content.find(['span'], string=['Date of birth:']).find_next('span').text
    date_of_birth = date_of_birth.strip().replace(',','').split(' ')
    month = date_of_birth[0]
    day = date_of_birth[1]
    year = date_of_birth[2]
    #print(year, '\n'+month, '\n'+day)
    return date_of_birth
  
  except:
    print(link+" player date of birth not found!")
    return np.nan


# + id="0pWzebPcbNEh"
# age
def player_age(page_content, link):
  try:
    age = page_content.find(['span'], string=['Age:']).find_next('span').text
    #print(age)
    return age
  
  except:
    print(link+" player age of birth not found!")
    return np.nan


# + [markdown] id="WAAJQZNEeCwo"
# ### height

# + id="A4kk5NS4eGKv"
def player_height (page_content, link):
  try:
    height = page_content.find(['span'], string=['Height:']).find_next('span').text
    #cleaning the text and cast it to int
    height = int(height.replace(',','').replace('m','').strip())
    #print(height)
    return height
  
  except:
    print(link+" player height not found!")
    return np.nan


# + [markdown] id="Gqaa1R3Pe_LH"
# ### citizenship

# + id="7NPajvXrfG3X"
def player_citizenship (page_content, link):
  try:
    citizenship = page_content.find(['span'], string=['Citizenship:']).find_next('span').text #all citizenships
    #print(citizanship.strip())
    citizenship = citizenship.strip().split('\xa0')
    return citizenship[0].strip() # first citizenship
  
  except:
    print(link+" player citizenship not found!")
    return np.nan


# + [markdown] id="oh8N8c-dgJLj"
# ### position

# + id="bFmJu8cGgL2r"
def player_position (page_content, link):
  try:
    position = page_content.find(['span'], string=['Position:']).find_next('span').text
    #cleaning the text 
    position = position.replace('-',' ')
    position = (" ".join(position.strip().split()))
    #print(position)
    return position
  
  except:
    print(link+" player position not found!")
    return np.nan


# + [markdown] id="ZqIsPGj7hJ8x"
# ### foot

# + id="8AIwFmZ2hRAs"
def player_foot (page_content, link):
  try:
    foot = page_content.find(['span'], string=['Foot:']).find_next('span').text
    #print(foot.strip())
    return foot
  
  except:
    print(link+" player foot not found!")
    return np.nan


# + [markdown] id="b2ezoJNdhqjm"
# ### player agent

# + id="nR4-Qwiuht5V"
def player_agent (page_content, link):
  try:
    player_agent = page_content.find(['span'], string=['Player agent:']).find_next('span').text
    #print(player_agent.strip())
    return player_agent.strip()
  
  except:
    print(link+" player agent not found!")
    return np.nan


# + [markdown] id="oQjYvZUNjDsq"
# ### current club

# + id="mL5obMDWjGCm"
def current_club(page_content, link):
  try:
    club_name = page_content.find('div', class_='data-header__club-info').find('span', class_='data-header__club').text
    #club_name = page.find('div', class_='data-header__club-info').find('span', class_='data-header__club').find('a')['title'] full name of club
    return club_name.strip()
  except:
    print(link+" current club not found!")
    return np.nan


# + [markdown] id="lpbNb-zSt04p"
# ### Detailed performance data

# + [markdown] id="GfRVTESH16QU"
# #### cast the table in website to pandas data frame to get more information

# + id="zblKixkcuSl3"
def detail_page_request(player_id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  #print (detail_link_format.format(id))
  detail_page=''
  try:
    detail_page = requests.get(detail_link_format.format(player_id), headers=headers)
    detail_page = BeautifulSoup(detail_page.content, 'html.parser') 
    return detail_page 
  except:
    print(detail_link_format.format(player_id)+" player detailed performance link not found!")
    return np.nan



# + id="oqa8W7T7Yf0H"
def create_player_detial_dataframe (id): # id is for returning an eeror 
  detail_page = detail_page_request(id)
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  # find table in html
  try:
    table = detail_page.find('table', class_='items')
  except:
    print(detail_link_format.format(id)+" detail table not found!")

  # find column names
  column_values=['player_id']
  try:
    header = detail_page.find('table', class_='items').find('thead').find('tr').find_all('th')
    for th in header:
      if th['id'] == 'yw1_c2':
        continue
      try:
        column_values.append(th.find('a').find('span')['title'])
      except:
        column_values.append(th.text)
    #print(column_values)
  except:
    print(detail_link_format.format(id)+" table column_value found!")

  # creat data frame 
  detail_table= pd.DataFrame(columns = column_values)

  # find table rows and add to dataframe 
  try:
    rows = detail_page.find('table', class_='items').find('tbody').find_all('tr')
    for row in rows:
      table_row = []
      table_row.append(id)
      for section in row.find_all('td'):
        if section.text !='':
          table_row.append(section.text)
        else:
          try:
            table_row.append(section.a['title'])
          except:
            continue
      detail_table.loc[len(detail_table.index)]= table_row  
  except:
    print(detail_link_format.format(id)+" table row not found!")

  return detail_table

  #find total row and add to dataframe
  '''
  total = []
  try:
    total_row = detail_page.find('table', class_='items').find('tfoot').find('tr').find_all('td')
    for row in total_row:
      try: 
        row['class']
        total.append(row.text)
      except:
        continue
  except:
    print(detail_link_format.format(id)+" total row not found!")
  detail_table.loc[len(detail_table.index)]= total
  '''
  return detail_table


# + id="2IQAo1Ovrn9u"
def detial_total_row(id):
  detail_page = detail_page_request(id)
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  total = []
  try:
    total_row = detail_page.find('table', class_='items').find('tfoot').find('tr').find_all('td')
    for row in total_row:
      try: 
        row['class']
        total.append(row.text)
      except:
        continue
  except:
    print(detail_link_format.format(id)+" total row not found!")
  return total



# + colab={"base_uri": "https://localhost:8080/"} id="sjlB00p6WLz9" outputId="297caaec-71bd-480a-ca83-b65478598847"
print(detial_total_row('17965'))


# + [markdown] id="jO7LsYW_t4JL"
# #### goals scored

# + id="_vGD0wcx2OhT"
def goals_scored (id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  try:
    return detial_total_row(id)[6]
  except:
    print(detail_link_format.format(id)+" goals scored not found!")
    return 'nan'



# + [markdown] id="6z06nf9ruFul"
# #### goals assisted

# + id="hWS5qxvV2d7e"
def goals_assisted (id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  try:
    return detial_total_row(id)[7]
  except:
    print(detail_link_format.format(id)+" goals assisted not found!")
    return 'nan'


# + [markdown] id="OrpkRTwNuJJg"
# #### total appearance

# + id="GWhJM7np2f66"
def total_appearance (id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  try:
    return detial_total_row(id)[4]
  except:
    print(detail_link_format.format(id)+" total appearance not found!")
    return 'nan'


# + [markdown] id="qc3vNF6JU9DN"
# #### goals_conceded

# + id="UAO49kXyVHq2"
def goals_conceded (id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  try:
    return detial_total_row(id)[13]
  except:
    print(detail_link_format.format(id)+" goals conceded not found!")
    return 'nan'


# + [markdown] id="6R5G4McmVPZF"
# #### clean_sheets

# + id="_KeAuT-HVSlf"
def clean_sheets (id):
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  try:
    return detial_total_row(id)[14]
  except:
    print(detail_link_format.format(id)+" clean sheats not found!")
    return 'nan'


# + [markdown] id="0llOB3U-6_q5"
# #### yello cards

# + id="PJLSPI_y7Ijm"
#print(total[11])

# + [markdown] id="asD-vqUq7tCB"
# #### second yellow cards

# + id="708TT-mx7ywT"
#print (total[12])

# + [markdown] id="dTBGQgPo73bZ"
# #### red cards

# + id="PmG3sRmf75SZ"
#print (total[13])

# + [markdown] id="Eone9167KBtW"
# ### transfer history

# + id="-ywC9eDqKEBq"
# creating a dataframe with the transfer history table 
def player_transfer_history_dataframe(page_content, link):
  try:
    html_transfer_table = page_content.find('div', class_='grid tm-player-transfer-history-grid tm-player-transfer-history-grid tm-player-transfer-history-grid--heading')
  except:
    print(link+" transfer table not found!")

  # create columns
  transfer_table_column= []
  transfer_table_column = html_transfer_table.text.split()
  transfer_table_column.append('player_id')
  #print(transfer_table_column)

  #create rows
  transfer_table_rows = []
  try:
    html_transfer_table_rows = page_content.find_all('div', class_='grid tm-player-transfer-history-grid')
    for row in html_transfer_table_rows:
      row= row.text
      #delete extra spaces
      row = re.sub(' +', '', row)
      #divide columns by \n
      row = row.split('\n')
      #delete empty strings from list
      row = list(filter(None, row))
      row.append(player_id(link))
      
      #
      transfer_table_rows.append(row)
  except:
    print(link+" transfer table rows not found!")
  
  transfer_table = pd.DataFrame(transfer_table_rows, columns =transfer_table_column)
  return transfer_table


# + [markdown] id="N8QztcLuZnpr"
# ##Crawler header

# + id="g0Ibd79Hqkyg"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language' : 'en-US,en;q=0.9'
}


# + [markdown] id="IvYcF2jHtLzf"
# ## Player information

# + id="MEMHAxJ21H81"
def player_info(page,link):
  info = []
  if player_position(page, link) == 'Goalkeeper':
    info.append(player_id(link))
    info.append(player_name(page, link))
    info.append(date_of_birth(page, link))
    info.append(player_height(page, link))
    info.append(player_citizenship(page, link))
    info.append(player_position(page, link))
    info.append(player_foot(page, link))
    info.append(current_club(page, link))
    info.append(goals_scored(player_id(link)))
    info.append(goals_assisted(player_id(link)))
    info.append(goals_conceded(player_id(link)))
    info.append(clean_sheets(player_id(link)))
    info.append(total_appearance(player_id(link)))
    info.append(player_agent(page, link))
  
  else: 
    info.append(player_id(link))
    info.append(player_name(page, link))
    info.append(date_of_birth(page, link))
    info.append(player_height(page, link))
    info.append(player_citizenship(page, link))
    info.append(player_position(page, link))
    info.append(player_foot(page, link))
    info.append(current_club(page, link))
    info.append(goals_scored(player_id(link)))
    info.append(goals_assisted(player_id(link)))
    info.append('nan')
    info.append('nan')
    info.append(total_appearance(player_id(link)))
    info.append(player_agent(page, link))
    
  return info


# + [markdown] id="uQgELewKaIQf"
# ###Creating tables related to players

# + id="22yreTHTtNj3"
# player table
#player, transfer
def find_player_info(link):
  page = requests.get(link, headers=headers)
  time.sleep(2)
  page = BeautifulSoup(page.content, 'html.parser')
  #print(page.prettify)
  player = []
  player_club = []
  player_statistics= pd.DataFrame()
  transfer = pd.DataFrame()

  #player table
  player = player_info(page, link)
  
  #transfer table
  

  return player, player_transfer_history_dataframe(page, link) , create_player_detial_dataframe(player_id(link))


# + [markdown] id="lAIEnoCOawG8"
# ##The process of finding the link of the players' page

# + [markdown] id="kZlD0r1gaphJ"
# ###1.Finding leagues of each season

# + id="VoIADfxmlze9"
# finding leagues of each season
def league_links (link):
  page = requests.get(link, headers=headers)
  page = BeautifulSoup(page.content, 'html.parser')
  #page.prettify
  leagues_link = []
  leagues={'First Tier', 'Second Tier', 'Third Tier', 'Fourth Tier', 'Fifth Tier'}
  tr_tags= page.find('table', class_= 'items').find('tbody').find_all('tr')
  flag = 2
  #for tr in tr_tags:

  for i, tr in enumerate(tr_tags):  
    #if i >1: 
      #break
    if(tr.find('td',class_='extrarow bg_blau_20 hauptlink') and tr.find('td',class_='extrarow bg_blau_20 hauptlink').text not in leagues):
      #print(tr.find('td',class_='extrarow bg_blau_20 hauptlink').text)
      flag =0
    elif (tr.find('td',class_='extrarow bg_blau_20 hauptlink') and tr.find('td',class_='extrarow bg_blau_20 hauptlink').text in leagues):
      flag = 1
    #if(tr.find('td', class_='hauptlink').find('tbody')):
    if(flag):
      try:
        lg_link = tr.find('td', class_='hauptlink').find('a')['href']
        #print(lg_link)
        leagues_link.append('https://www.transfermarkt.com'+lg_link)
      except:
        continue
  return leagues_link


# + [markdown] id="0S5FztpnbCAg"
# ###2.Finding teams of each league

# + id="uDSd8m54H9Nk"
#find teams of each league 
def team_links(link): #link of the league teams page
  page = requests.get(link, headers=headers)
  page = BeautifulSoup(page.content, 'html.parser')
  try:
    team_tag = page.find('table', class_='items').find('tbody').find_all('tr')
  except:
    print(link+ ' team table not found!')
  team_link =[]
  for i, tr in enumerate(team_tag):
    #if i>2:
     #break
    try:
      team_link.append('https://www.transfermarkt.com'+tr.find('td').find_next('td').find('a')['href'])
    except:
      print(link+ ' team link not found')
      team_link.append(np.nan)
  
  return team_link


# + [markdown] id="Y4EvcIRHbLnz"
# ###3.finding players of each team

# + id="3AXc8XxgMvGU"
# find players link by team link
def player_links(link): 
  page = requests.get(link, headers=headers)
  time.sleep(2)
  page = BeautifulSoup(page.content, 'html.parser')

  players_link=[]
  player_tag = page.find('table', class_='items').find('tbody').find_all('tr')
  for tr in player_tag:
    #if len(players_link)>9:
      #break
    try:
      player_link= tr.find('table', class_='inline-table').find('td', class_='hauptlink').find('div', class_='di nowrap').find('a')['href']
      players_link.append('https://www.transfermarkt.com'+ player_link)
    except:
      #print('player link not found')
      continue
    #print(player_name)
  
  return players_link



# + [markdown] id="XGI0q_8DbVK6"
# ##Crawling main code

# + id="vxpzxgpniJ9L"
country_season_link_format = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}/saison_id/{}/plus/1'
#country_id = {'189', '50', '157', '40', '75'} #England, France, Spain, Germany, Italy
country_id = {'189'} #England, France
season = {'2021'}

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

#final tables (all datas from players)
player_table = pd.DataFrame(columns = player_table_culomns)
transfer_table = pd.DataFrame(columns = transfer_table_culomns)


for c_id in tqdm(country_id, desc ="countries"):
  
  for i, s_id in enumerate(season):
    link = country_season_link_format.format(c_id, s_id)
    
    all_season_leagues=(league_links(link))
    print('----- leagues links',all_season_leagues)
    
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
              player, transfer = find_player_info(player_link)
              
              player_table.loc[len(player_table.index)]= player
              transfer_table = pd.concat([transfer_table, transfer], axis=0)
            else:
              print(player_link + ' duplicate id found and skiped')
            continue
          except:
            print(player_link + ' something wrong and skiped')           
            continue
          


player_table.to_csv('player_table.csv', encoding='utf-8')
transfer_table.to_csv('trasnfer_table.csv', encoding='utf-8')
#df.to_csv(file_name, sep='\t', encoding='utf-8')


# + [markdown] id="hF0b2mtHxrka"
# # Test area

# + id="b81_gHjy0vHF"
def test (id): # id is for returning an eeror 
  detail_page = detail_page_request(id)
  detail_link_format = 'https://www.transfermarkt.com/ruben-dias/leistungsdatendetails/spieler/{}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
  # find table in html
  try:
    table = detail_page.find('table', class_='items')
  except:
    print(detail_link_format.format(id)+" detail table not found!")

  # find column names
  column_values=['player_id']
  try:
    header = detail_page.find('table', class_='items').find('thead').find('tr').find_all('th')
    for th in header:
      if th['id'] == 'yw1_c2':
        continue
      try:
        column_values.append(th.find('a').find('span')['title'])
      except:
        column_values.append(th.text)
    #print(column_values)
  except:
    print(detail_link_format.format(id)+" table column_value found!")

  # creat data frame 
  detail_table= pd.DataFrame(columns = column_values)

  # find table rows and add to dataframe 
  try:
    rows = detail_page.find('table', class_='items').find('tbody').find_all('tr')
    for row in rows:
      table_row = []
      table_row.append(id)
      for section in row.find_all('td'):
        if section.text !='':
          table_row.append(section.text)
        else:
          try:
            table_row.append(section.a['title'])
          except:
            continue
      detail_table.loc[len(detail_table.index)]= table_row  
  except:
    print(detail_link_format.format(id)+" table row not found!")

  return detail_table


# + id="LAYf53cFnMMG"
id = ['357885', '120629']
table = pd.DataFrame()
for i in id:
  table = pd.concat([table, test(i)], axis=0)
table.head
table.to_csv('stat_test1.csv', encoding='utf-8')


# + [markdown] id="eTlA_fkhmllh"
# ## Creting Test .csv files 

# + id="fnAooFxDnu_5"
# find the first two league of each season for test
def first_two_league (link):
  page = requests.get(link, headers=headers)
  page = BeautifulSoup(page.content, 'html.parser')
  #page.prettify
  leagues_link = []
  leagues={'First Tier', 'Second Tier', 'Third Tier', 'Fourth Tier', 'Fifth Tier'}
  tr_tags= page.find('table', class_= 'items').find('tbody').find_all('tr')
  flag = 2
  #for tr in tr_tags:

  for i, tr in enumerate(tr_tags):  
    if i >1: 
      break
    if(tr.find('td',class_='extrarow bg_blau_20 hauptlink') and tr.find('td',class_='extrarow bg_blau_20 hauptlink').text not in leagues):
      #print(tr.find('td',class_='extrarow bg_blau_20 hauptlink').text)
      flag =0
    elif (tr.find('td',class_='extrarow bg_blau_20 hauptlink') and tr.find('td',class_='extrarow bg_blau_20 hauptlink').text in leagues):
      flag = 1
    #if(tr.find('td', class_='hauptlink').find('tbody')):
    if(flag):
      try:
        lg_link = tr.find('td', class_='hauptlink').find('a')['href']
        #print(lg_link)
        leagues_link.append('https://www.transfermarkt.com'+lg_link)
      except:
        continue
  return leagues_link


# + id="lFMcilchnEE5"
#find the first three team of each league for test
def first_three_team(link): #link of the league teams page
  page = requests.get(link, headers=headers)
  page = BeautifulSoup(page.content, 'html.parser')
  try:
    team_tag = page.find('table', class_='items').find('tbody').find_all('tr')
  except:
    print(link+ ' team table not found!')
  team_link =[]
  for i, tr in enumerate(team_tag):
    if i>2:
      break

    try:
      team_link.append('https://www.transfermarkt.com'+tr.find('td').find_next('td').find('a')['href'])
    except:
      print(link+ ' team link not found')
      team_link.append(np.nan)
  
  return team_link


# + id="OPktOnztsOeu"
# find first 10 players link by team link
def first_ten_players(link): 
  page = requests.get(link, headers=headers)
  time.sleep(2)
  page = BeautifulSoup(page.content, 'html.parser')

  players_link=[]
  player_tag = page.find('table', class_='items').find('tbody').find_all('tr')
  for tr in player_tag:
    if len(players_link)>9:
      break
    try:
      player_link= tr.find('table', class_='inline-table').find('td', class_='hauptlink').find('div', class_='di nowrap').find('a')['href']
      players_link.append('https://www.transfermarkt.com'+ player_link)
    except:
      #print('player link not found')
      continue
    #print(player_name)
  
  return players_link



# + id="C_jwkujqpM4h"
country_season_link_format = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}/saison_id/{}/plus/1'
#country_id = {'189', '50', '157', '40', '75'} #England, France, Spain, Germany, Italy
country_id = {'189'} #England, France
season = {'2021'}

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
statistics_table= pd.DataFrame()


for c_id in tqdm(country_id, desc ="countries"):
  
  for i, s_id in enumerate(season):
    link = country_season_link_format.format(c_id, s_id)
    
    all_season_leagues=(first_two_league(link))
    print('----- leagues links',all_season_leagues)
    
    for league_link in tqdm(all_season_leagues, desc='leagues'):
      #print(league_link)
      all_league_teams=(first_three_team(league_link))
      #print('-------- leage teams',all_league_teams)
      #for team_link in tnrange(all_league_teams, desc ="teams"):
      for team_link in tqdm(all_league_teams, desc='teams'):  
       
        all_team_players=(first_ten_players(team_link))
        for player_link in (all_team_players):
          #print('player info: find_player_info')
          #print(player_link)
          #print(find_player_info(player_link))
          try:
            if player_id(player_link) not in player_ids:
              player_count+=1
              #print ('new id added','   ',player_count,'  ', player_id(player_link))
              player_ids.append(player_id(player_link))
              player, transfer, statistics = find_player_info(player_link)
              
              player_table.loc[len(player_table.index)]= player
              transfer_table = pd.concat([transfer_table, transfer], axis=0)
              statistics_table = pd.concat([statistics_table, statistics], axis=0)
            else:
              print(player_link + ' duplicate id found and skiped')
            continue
          except:
            print(player_link + ' something wrong and skiped')           
            continue
          


player_table.to_csv('test_player_table.csv', encoding='utf-8')
transfer_table.to_csv('test_trasnfer_table.csv', encoding='utf-8')
statistics_table.to_csv('test_statistics_table.csv', encoding='utf-8')
#df.to_csv(file_name, sep='\t', encoding='utf-8')

    


# + [markdown] id="Pim1x5HnCAUW"
# ## test area for test tables

# + id="gJKEBc5d6tEj"
links= ['https://www.transfermarkt.com/manuel-neuer/profil/spieler/17259', 'https://www.transfermarkt.com/david-alaba/profil/spieler/59016','https://www.transfermarkt.com/jerome-boateng/profil/spieler/26485']

#final tables culomns & Each player's table
player_table_culomns = ['player_id', 'name', 'birth_date', 'height', 'current_international', 'main_position', 'foot', 'current_club', 'goals_scored', 'goals_assisted', 'goals_conceded', 'clean_sheets', 'total_appearence', 'agent']
transfer_table_culomns = ['player_id','season', 'date', 'left', 'joined', 'MV', 'Fee']

player = pd.DataFrame(columns = player_table_culomns)
transfer = pd.DataFrame()

#test variables
player_ids=[]
player_count=0

#final tables (all datas from players)
player_table = pd.DataFrame(columns = player_table_culomns)
transfer_table = pd.DataFrame(columns = transfer_table_culomns)


all_league_teams= ['https://www.transfermarkt.com/manchester-city/startseite/verein/281/saison_id/2019','https://www.transfermarkt.com/fc-watford/startseite/verein/1010/saison_id/2019','https://www.transfermarkt.com/norwich-city/startseite/verein/1123/saison_id/2019']
#print('player info list ',player)
#print('transfer dataframe ', transfer)
for team_link in tqdm(all_league_teams, desc='teams'):       
  all_team_players=(first_ten_players(team_link))
  for player_link in tqdm(all_team_players):
    page = requests.get(player_link, headers=headers)
    page = BeautifulSoup(page.content, 'html.parser')

    try:
        if player_id(player_link) not in player_ids:
            player_count+=1
            #print ('new id added','   ',player_count,'  ', player_id(player_link))
            player_ids.append(player_id(player_link))
            player, transfer = find_player_info(player_link)
        else:
          print(player_link + ' duplicate id found and skiped')
          continue
    except:
      print(player_link + ' something wrong and skiped')           
      continue
    player_table.loc[len(player_table.index)]= player
    transfer_table = pd.concat([transfer_table, transfer], axis=0)
  #transfer_table = pd.concat([transfer_table, transfer], axis=0)

print(player_table)
player_table.to_csv('only for test2.csv', encoding='utf-8')
#print(transfer_table)
