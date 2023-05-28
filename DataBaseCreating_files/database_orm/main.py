# +
from core import Awards, Award_winners, Club
from utils import *
import pandas as pd
import os


engine = get_engine(db='quera_project1')


df_awards = pd.read_csv( os.path.join(os.path.dirname(__file__), "../preprocessing/final csv/Awards.csv"))
df_award_winners = pd.read_csv( os.path.join(os.path.dirname(__file__), "../preprocessing/final csv/Awards_winners.csv"))
df_club = pd.read_csv( os.path.join(os.path.dirname(__file__), "../preprocessing/final csv/Club_table.csv"))
df_club_stats = pd.read_csv( os.path.join(os.path.dirname(__file__), "../preprocessing/final csv/Clubs_stats.csv"))

with engine.connect() as connection :
    df_club =df_club.drop_duplicates(subset=['id'])
    df_club.to_sql(name='club', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('club inserted to database')

    df_awards.to_sql(name='awards', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('awards inserted to database')

    df_award_winners.to_sql(name='award_winners', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('award winners inserted to database')

    # df_club.head(5)


    df_club_stats.rename(columns={'Season': 'season', 
    'id':'club_id',
    'ARRIVALS':'arrivals',
    'DEPARTURES':'departures',
    'Average age of players':'player_avg_age',
    'League name':'league_name',
    'Total market value':'total_market_value'
    }, inplace=True)
    df_club_stats.head(5)
    df_club_stats.to_sql(name='club_stats', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('club stats inserted to database')



