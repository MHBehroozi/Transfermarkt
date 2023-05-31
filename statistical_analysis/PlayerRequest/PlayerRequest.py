# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # import Libraries

# +
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import text
from urllib.parse import quote_plus
# -

# # create sql URL

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="",
    host="localhost"
    )

# # create sengine

engin = create_engine(url_object)

# # Fetch the required DATA

query = ('''SELECT `club_full_name`, `club_id`,sum(PPG) as PPG, sum(goals) as goals,sum(own_goals) as own_goals,sum(yellow_cards) as yellow_cards,sum(second_yellow_cards) as second_yellow_cards,sum(red_cards) as red_cards,sum(clean_sheets) as clean_sheets, sum(goals_conceded) as goals_conceded, sum(assists) as assists,sum(minutes_per_goal) as minutes_per_goal FROM `player_statistics` 
WHERE season =2021 and appearances !=0 and competition in ('Premier League', 'Bundesliga', 'Serie A', 'Ligue 1', 'LaLiga') 
GROUP BY club_full_name;''') 

with engin.connect() as conn:
    conn.execute(text("USE quera_project1"))
    df = pd.read_sql(text(query), conn)
    df = df.fillna(0)

df.head(200)

# # Normalize columns
#

# +


import pandas as pd
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
df_normalized = pd.DataFrame(scaler.fit_transform(df[numeric_columns]), columns=numeric_columns)

df_final = pd.merge(df['club_full_name'], df_normalized, left_index=True, right_index=True)

df_final.head()

# +
pos_attack_metrics = [ "goals", "assists", "PPG"]
pos_attack_weight = [ 70, 30,10 ]

neg_attack_metrics = ["minutes_per_goal"]
neg_attack_weight = [20]

pos_defence_metrics = [ "clean_sheets" ]
pos_defence_weight = [ 50 ]
neg_defence_metrics = ["own_goals", "yellow_cards", "second_yellow_cards", "red_cards", "goals_conceded"]
neg_defence_weight = [10, 10, 10, 30, 40]


def attack_metric(row):
    row['attack_metric'] = sum([pos_attack_weight[i] * row[pos_attack_metrics[i]] for i in range(len(pos_attack_metrics))]) - sum([neg_attack_weight[i] * row[neg_attack_metrics[i]] for i in range(len(neg_attack_metrics))])

    total_weight = sum(pos_attack_weight) + sum(neg_attack_weight)
    row['attack_metric'] = row['attack_metric']/total_weight
    return row['attack_metric']

def defence_metric(row):
    row['defence_metric'] = sum([pos_defence_weight[i] * row[pos_defence_metrics[i]] for i in range(len(pos_defence_metrics))]) - sum([neg_defence_weight[i] * row[neg_defence_metrics[i]] for i in range(len(neg_defence_metrics))])
    total_weight = sum(pos_defence_weight) + sum(neg_defence_weight)
    row['defence_metric'] = row['defence_metric']/total_weight
    return row['defence_metric']


# -

attack_metric(df_final)
defence_metric(df_final)
df_final.head(5)


# +
df_final[['club_full_name', 'attack_metric', 'defence_metric']].sort_values(by=['attack_metric', 'defence_metric'],
                             ascending=[False, True])
# df_final['defence_attack_diff'] =  df_final['attack_metric'] -  df_final['defence_metric']

# df_final[['club_full_name', 'defence_attack_diff']].sort_values(by=['defence_attack_diff'],
#                              ascending=[False])

# -

df_final[['club_full_name', 'defence_attack_diff']].to_csv('player_request.csv', index=False)

# !jupytext --to py -o PlayerRequest.py PlayerRequest.ipynb
