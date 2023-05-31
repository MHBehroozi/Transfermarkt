import streamlit as st
import pandas as pd


st.set_page_config(
    page_title='Transfermarkt',
    page_icon= ':soccer:'
)
st.title("Part 2: Designing DataBase and ORM")

st.header('Data Preprocessing')
"""
To insert Data into the Database and use it in the following analysis, we should clean and preprocess crawled Data. This operation has been done in two parts. At first, The data were checked directly, their datatype was modified, some features were removed, added or changed, and if needed, they were broken down into more tables. In next part, when adding data to the Database using ORM, it was checked that the duplicate record is not entered into the Database.

You can see part of the code related to direct preprocessing at below:
"""

st.subheader('Awards and Cups')
"""
In this section, `Cups_winners` between the seasons 2015/16 to 2021/22 was filtered and divided into two tables `Awards` and `Award_Winners`. In total, we have 29 records for Awards and 166 records for Award Winners.
"""
cup_winners_selected = pd.read_csv('.\WebScraping_data\Cup_crawl\cup_winners_selected.csv') 
cup_name=cup_winners_selected['cup_name'].unique()
awards_id=[]
awards=[]

for i in range(len(cup_name)):
    award=cup_name[i]
    award_id='A-'+ str(i+1)
    awards_id.append(award_id)
    awards.append(award)

dic={}
dic['award_id'] = awards_id
dic['cup_name'] = awards

df = pd.DataFrame(data=dic)

st.code("""
cup_winners_selected = cup_winners[cup_winners.win_year_from >= 2015 & cup_winners.win_year_to <= 2022]
cup_name=cup_winners_selected['cup_name'].unique()
awards_id=[]
awards=[]

for i in range(len(cup_name)):
    award=cup_name[i]
    award_id='A-'+ str(i+1)
    awards_id.append(award_id)
    awards.append(award)

dic={}
dic['award_id'] = awards_id
dic['cup_name'] = awards

df = pd.DataFrame(data=dic)
df.to_csv('Awards.csv', index=False)
""",
    language="python")

merged_df=cup_winners_selected.merge(df, on='cup_name', how='left')
merged_df.drop(['win_year_to'],axis=1,inplace=True)
merged_df.rename(columns = {'win_year_from':'win_year'}, inplace = True)
merged_df.drop(['club_name'],axis=1,inplace=True)
merged_df.drop(['cup_name'],axis=1,inplace=True)

st.code("""
merged_df=cup_winners_selected.merge(df, on='cup_name', how='left')
merged_df.drop(['win_year_to'],axis=1,inplace=True)
merged_df.rename(columns = {'win_year_from':'win_year'}, inplace = True)
merged_df.drop(['club_name'],axis=1,inplace=True)
merged_df.drop(['cup_name'],axis=1,inplace=True)
merged_df.to_csv('Awards_winners.csv', index=False)
""",
    language="python")

'**Awards table:**'
st.dataframe(df)

'**Award_winners table:**'
st.dataframe(merged_df)


"---------"

st.subheader('Merging Club dataframes')
"""
As you can see [here](https://github.com/MHBehoozi/Transfermarkt/tree/master/WebScraping_data/League_crawl), Leagues Data contains five country premier leagues and seasons during 2015/16 to 2021/22. Also we'd need to have league table which contains Clubs for each country and a table for Clubs Statistics.

In total, 147 records for clubs and 686 records for club statistics have been extracted
"""

st.code("""
# read all csv files for spain: Laliga

laliga_2015=pd.read_csv('laliga_2015.csv')
laliga_2015['Season']='2015'
laliga_2016=pd.read_csv('laliga_2016.csv')
laliga_2016['Season']='2016'
laliga_2017=pd.read_csv('laliga_2017.csv')
laliga_2017['Season']='2017'
laliga_2018=pd.read_csv('laliga_2018.csv')
laliga_2018['Season']='2018'
laliga_2019=pd.read_csv('laliga_2019.csv')
laliga_2019['Season']='2019'
laliga_2020=pd.read_csv('laliga_2020.csv')
laliga_2020['Season']='2020'
laliga_2021=pd.read_csv('laliga_2021.csv')
laliga_2021['Season']='2021'

Spain=pd.concat([laliga_2015,laliga_2016,laliga_2017,laliga_2018,laliga_2019,laliga_2020,laliga_2021])
Spain.drop(['Unnamed: 0'],axis=1,inplace=True)
""")

'This work has also been done for other countries, whose codes are not given due to brevity.'

st.code("""
# merge all country leagues

Clubs_df = pd.concat([Spain,England,Germany,France,Italy],ignore_index=True)
Clubs_df.rename(columns = {'Club Values':'Total market value','Coach Date':'Appointed Date'}, inplace = True)
Clubs_df['Appointed Date'] = Clubs_df['Appointed Date'].astype('datetime64[ns]') 
Clubs_df['Total market value']=Clubs_df['Total market value'].str.replace('€','')
Clubs_df.to_csv('Clubs_df.csv', index=False)
""")

st.code("""
# make table fo clubs stats

balance=pd.read_csv('over_all_balance.csv')
balance.rename(columns = {'Club':'Club Name'}, inplace = True)
balance['Season']=balance['Season'].astype(str)

Clubs_df['Season']=Clubs_df['Season'].astype(str)

merged=balance.merge(Clubs_df,on=['Season','Club Name'],how='left')
merged.drop(['Country_x','link','Club Name','Country_y'],axis=1,inplace=True)
merged['expend']=merged['expend'].str.replace('€','') 
merged['income']=merged['income'].str.replace('€','') 
merged['overall_balance']=merged['overall_balance'].str.replace('€','') 
merged.to_csv('Clubs_stats.csv', index=False)
""")

'**Club table:**'
Clubs_df = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\Club_table.csv')
st.dataframe(Clubs_df)

'**Club_stats table:**'
merged = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\Clubs_stats.csv')
st.dataframe(merged)

"---------"

st.subheader('Coach Table')
"""
Coaches Data is extracted from Club pages. In total we have 415 records for coaches.
"""

st.code("""
Coach_table=pd.DataFrame()
Coach_table['Club Name']=Clubs_df['Club Name']
Coach_table['Coach name']=Clubs_df['Coach name']
Coach_table['Appointed Date']=Clubs_df['Appointed Date']
Coach_table=Coach_table.drop_duplicates(keep='last')

coach_df=Coach_table.merge(club_table,on='Club Name',how='left')
coach_df.drop(['Club Name','Country'],axis=1,inplace=True)
coach_df.to_csv('coach_df.csv', index=False)
""")

'**coach table:**'
coach_df = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\coach_df.csv')
st.dataframe(coach_df)

"---------"

st.subheader('Stadium Table')
"""
Such as Coaches Data, Stadium Data is extracted from Club pages. In total we have 145 records for stadiums.
"""
st.code("""
Stadium_df=pd.DataFrame()
Stadium_df['Club Name']=Clubs_df['Club Name']
Stadium_df['Stadium name']=Clubs_df['Stadium name']
Stadium_df=Stadium_df.drop_duplicates(keep='last')

Stadium_table=Stadium_df.merge(club_table,on='Club Name',how='left')
Stadium_table.drop(['Country','Club Name'],axis=1,inplace=True)
Stadium_table.rename(columns = {'id':'Club_id'} , inplace = True)

index=Stadium_table[Stadium_table['Club_id'].isnull()].index.tolist()
Stadium_table.drop(index,axis=0,inplace=True)

Stadium_table.to_csv('Stadium_table.csv', index=False)
""")
'**Stadium table:**'
Stadium_table = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\Stadium_table.csv')
st.dataframe(Stadium_table)

"---------"

st.subheader('Player Tables')
"""
Player Data preprocessing section has more codes. You can refer to this [link](https://github.com/MHBehoozi/Transfermarkt/blob/master/DataBaseCreating_files/preprocessing/players_data_cleaning.ipynb) to check the complete codes. The result of this section is the creation of three tables:
* Player table
* Player_statistics
* player_transfers

In the following, part of the codes of this part will be checked. In total, 9,365 records for players, 59,860 records for statistics and 78,987 records for transfers have been extracted.
"""

st.code("""
# player table

# merge all crawled data
merged=pd.concat([df157,df189,df40,df50,df75],axis=0,ignore_index=True)

# initial preprocessing
merged.drop(['Unnamed: 0'],axis=1,inplace=True)
merged['birth_date']=merged['birth_date'].str.replace('[','').str.replace(']','').str.replace("'","").str.replace(', Happy, Birthday','')
merged['birth_date']=merged['birth_date'].astype('datetime64[ns]') 
index=merged[merged['main_position']!='Goalkeeper'].index
merged['goals_conceded'].loc[index]=merged['goals_conceded'].loc[index].replace(np.nan,'-')
merged['clean_sheets'].loc[index]=merged['clean_sheets'].loc[index].replace(np.nan,'-')
merged.drop_duplicates(keep='last',inplace=True)

# remove redundant features
merged.drop(['current_international','current_club','goals_scored','goals_assisted','goals_conceded','clean_sheets','total_appearence'],axis=1, inplace=True)
merged.to_csv('palyers.csv')
""")

st.code("""
# palyers_statistics table

# club table with IDs
clubs=pd.read_csv('club_ids101.csv')
clubs.drop(['Unnamed: 0'],axis=1,inplace=True)

# merge players with clubs
df=merged.merge(clubs,how='left', on='current_club')
df.drop(['club full name'],axis=1,inplace=True)

# import statistics data
df3=pd.read_csv('statistics table40.csv')
...
df2=pd.read_csv('statistics table189.csv')

# concat imported data
palyers_statistic=pd.concat([df1,df2,df3,df4,df5],ignore_index=True)
palyers_statistic.drop_duplicates(keep='last',inplace=True)
palyers_statistic=palyers_statistic.merge(clubs,how='left', on='club full name')

# replace NaN values and modify datatypes
for column in columns:
   palyers_statistic[column]=palyers_statistic[column].replace('-',0)

for column in columns[4:-1]:
  print(column)
  palyers_statistic[column]=palyers_statistic[column].replace('0,00','0') 
  palyers_statistic[column]=palyers_statistic[column].astype(str)
  palyers_statistic[column]=palyers_statistic[column].apply(lambda x: x.strip(" \' ") if x!=0 else x)
  palyers_statistic[column]=palyers_statistic[column].astype(float)

# import market_value for players
market_value=pd.read_csv('market_value_df.csv')

# add market_value to palyers_statistic
df=palyers_statistic.merge(market_value, on=['season','player_id'], how='left')
df.drop(['Unnamed: 0'],axis=1,inplace=True)
df.to_csv('palyers_statistic.csv',index=False)
""")

st.code("""
# player_transfers table

# import crawled data
merged=pd.read_csv('transfer_history.csv')

# add required features
merged['transfer/loan']=merged['Loan_Fee'].apply(lambda x: 1 if x=='-' else 0)

# modify features
merged['Loan_Fee']=merged['Loan_Fee'].apply(lambda x: 0 if x=='-' else x)
merged['Loan_Fee']=merged['Loan_Fee'].astype(float)
merged['Transfer_Fee']=merged['Transfer_Fee'].apply(lambda x: np.nan if x=='draft' else x)
merged['Transfer_Fee']=merged['Transfer_Fee'].apply(lambda x:0 if x=='free transfer' else 0 if x=='loan transfer' else 0 if x=='-' else float(x))
merged['MV']=merged['MV'].apply(lambda x: 0 if x=='-' else x)

# modify features
columns=merged.columns
for column in columns[1:3]:
  merged[column]=merged[column].astype(float)
merged['Loan_Fee']=merged['Loan_Fee'].astype(float)

merged.to_csv('transfer_players.csv',index=False)
""")

'**Players table:**'
table = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\palyers.csv').drop(columns=['Unnamed: 0'])
st.dataframe(table)

'**Player_statistics table:**'
table = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\palyers_statistic.csv')
st.dataframe(table)

'**Player_transfers table:**'
table = pd.read_csv(r'.\DataBaseCreating_files\preprocessing\final csv\transfer_players.csv')
st.dataframe(table)


"---------"

st.header('Database Design')
st.subheader('Database Diagram')
"""
In this project, a MySQL Database has used to store data. As we described in the preprocessing section, we have 9 tables in our Database:
1. award_winners
1. awards
1. club
1. club_stats
1. coach
1. player
1. player_statistics
1. player_transfers
1. stadium
"""

"---------"
st.subheader('ORM and Inserting Data into Database')
"""
For creating tables and inserting data into the database, after creating the schema, **ORM** has been used. For this purpose, three module has been defined:
* [main.py](https://github.com/MHBehoozi/Transfermarkt/blob/master/DataBaseCreating_files/database_orm/main.py)
* [core.py](https://github.com/MHBehoozi/Transfermarkt/blob/master/DataBaseCreating_files/database_orm/core.py)
* [utils.py](https://github.com/MHBehoozi/Transfermarkt/blob/master/DataBaseCreating_files/database_orm/utils.py)

`core.py` contains classes for each table that contain all the attributes and columns of that table. These classes will be used to create Database tables.

By running `main.py`, this module will make a connection with Database, will use `core.py` module to create tables and will insert preprocessed data into tables.

`utils.py` is the module that has functions for creating connection with Database and updating Data which `main.py` use them for it's purpose.
"""