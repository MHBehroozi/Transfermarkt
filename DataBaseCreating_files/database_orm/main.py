# +
from core import Awards, Award_winners, Club
from utils import *
import pandas as pd
import os


engine = get_engine(db='quera_project1')


dirname = os.path.dirname(__file__)
df_awards = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/Awards.csv"))
df_award_winners = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/Awards_winners.csv"))
df_club = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/Club_table.csv"))
df_club_stats = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/Clubs_stats.csv"))
df_coach = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/coach_df.csv"))
df_stadium = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/Stadium_table.csv"))

with engine.connect() as connection :
 
    # club
    df_club =df_club.drop_duplicates(subset=['id'])
    df_club.to_sql(name='club', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('club inserted to database')

    # awards
    df_awards.to_sql(name='awards', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('awards inserted to database')

    # award winners
    df_award_winners.to_sql(name='award_winners', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('award winners inserted to database')

    # club statistics
    df_club_stats.rename(columns={'Season': 'season', 
    'id':'club_id',
    'ARRIVALS':'arrivals',
    'DEPARTURES':'departures',
    'Average age of players':'player_avg_age',
    'League name':'league_name',
    'Total market value':'total_market_value'
    }, inplace=True)

    df_club_stats.to_sql(name='club_stats', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('club stats inserted to database')

    # Coach
    df_coach.rename(columns={ 
    'Coach name':'coach_name',
    'Appointed Date':'appointed_date',
    'id':'club_id',
    }, inplace=True)
    df_coach.to_sql(name='coach', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('coach inserted to database')

    # stadium
    df_stadium.rename(columns={ 
    'Stadium name':'stadium_name',
    }, inplace=True)
    df_stadium.to_sql(name='stadium', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('stadium inserted to database')




