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
df_player = pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/palyers.csv"))
df_player_stats= pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/palyers_statistic.csv"))
df_player_transfers= pd.read_csv( os.path.join(dirname, "../preprocessing/final csv/transfer_players.csv"))

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
    df_award_winners.drop('nation', axis=1, inplace=True)
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

    # player
    df_player = df_player.drop(df_player.columns[[0]], axis=1) # df.columns is zero-based pd.Index
    df_player =df_player.drop_duplicates(subset=['player_id'])
    df_player.rename(columns={ 
    'player_id':'id',
    }, inplace=True)
    df_player.to_sql(name='player', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('player inserted to database')



    # player statistics
    #player_id,season,Competition,club full name,Squad,Appearances,PPG,Goals,Own goals,Substitutions on,Substitutions off,Yellow cards,
    # Second yellow cards,Red cards,Goals conceded,
    # Clean sheets,Minutes played,Assists,Penalty goals,Minutes per goal,club_id,club name,market_value

    df_player_stats.rename(columns={ 
    'Competition':'competition',
    'club full name':'club_full_name',
    'Squad':'squad',
    'Appearances':'appearances',
    'Goals':'goals',
    'Own goals':'own_goals',
    'Substitutions on':'substitutions_on',
    'Substitutions off':'substitutions_off',
    'Yellow cards':'yellow_cards',
    'Second yellow cards':'second_yellow_cards',
    'Red cards':'red_cards',
    'Goals conceded':'goals_conceded',
    'Clean sheets':'clean_sheets',
    'Minutes played':'minutes_played',
    'Assists':'assists',
    'Penalty goals':'penalty_goals',
    'Minutes per goal':'minutes_per_goal',
    'club name':'club_name',
    }, inplace=True)

    df_player_stats =df_player_stats.drop_duplicates(subset=['club_id', 'player_id', 'season', 'competition'])
    df_player_stats.to_sql(name='player_statistics', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('player statistics inserted to database')

    # df_player_transfers
    df_player_transfers.rename(columns={ 
    'Transfer_Fee':'transfer_Fee',
    'Date':'date',
    'Loan_Fee':'loan_Fee',
    'transfer/loan':'transfer_loan',
    }, inplace=True)
    df_player_transfers.to_sql(name='player_transfers', con=connection, schema='quera_project1', if_exists='append',\
                index=False, method='multi', chunksize=12)
    connection.commit()
    print('player transfer inserted to database')


