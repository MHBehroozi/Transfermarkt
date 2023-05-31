import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config(
    page_title='Transfermarkt',
    page_icon= ':soccer:'
)
st.title("Part 3: Statistical Analysis")
"""
In this part, we'd like to answer a number of questions with the help of statistical knowledge; Some questions have been asked to understand and find intuition from the data, others from the side of a particular person, and at the end a number of hypotheses have been proposed, and the validity of these hypotheses is examined in this section.
"""

st.header('Descriptive Statistics')
'This section has 6 questions which need understanding the data and working with it. Also, it is necessary to draw diagrams to analyze the problems.'
'You can check Jupyter notebook for this part in this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/Descriptive%20Statistics)'

st.subheader('Question 1: Distribution of the number of games played by players in season 2021/22')

'In this question, `Appearances` is used for players. After removing the outlier data, the common statistical probability distributions were checked on this feature. Python Fitter library has been used for this purpose'

part1_table = pd.read_csv(r'.\statistical_analysis\Descriptive Statistics\exported_data\part1_table.csv')
st.table(part1_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part1_diagram.png')
st.image(image)

'Also you can see similar information for the proportion of players appearances in games in the following'

part1_2_table = pd.read_csv(r'.\statistical_analysis\Descriptive Statistics\exported_data\part1_2_table.csv')
st.table(part1_2_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part1_2_diagram.png')
st.image(image)

st.subheader('Question 2: The relationship between the number of goals scored and the estimated market value for a player in season 2021/22')

'In this question, after removing outliers, we are going to draw a scatter plot between `players total goals` and `players market value` and try to draw linear regression between them. Parameters of linear regression have been estimatred using `stats.linregress()`'
'As you can see, there is no linear relation between them:'
image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part2_diagram.png')
st.image(image)

st.subheader('Question 3: The relationship between the number of goals scored and the estimated market value for a striker in season 2021/22')

'In this question, after removing outliers, we are going to draw a scatter plot between `strikers total goals` and `strikers market value` and try to draw linear regression between them. Parameters of linear regression have been estimatred using `stats.linregress()`'
'As you can see, there is no linear relation between them:'
image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part3_diagram.png')
st.image(image)

st.subheader('Question 4: Distribution of player estimated market value by position in season 2021/22')

'After removing the outlier data, boxplot digram of estimated market value has been drawn for each position'

image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part4_diagram.png')
st.image(image)

# st.subheader('Question 5: The total number of goals scored in each leagues in season 2021/22')
# 'After removing the outlier data, bar chart of total goals scored has been drawn for each league'

st.subheader('Question 5: Distribution of goals scored in each leagues in season 2021/22')
'You can see total goals in each league in season 2021/22 in the following:'

image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part5_diagram.png')
st.image(image)

st.subheader('Question 6: The distribution of the total amount of money that the clubs had to spend to buy players during seasons 2017/18 to 2021/22')
'For this question, first, the total amount of money that the clubs had to spend to buy players in each season has computed. Next, after removing outliers, the common statistical probability distributions were checked on this feature. Python Fitter library has been used for this purpose'

part6_table = pd.read_csv(r'.\statistical_analysis\Descriptive Statistics\exported_data\part6_table.csv')
st.table(part6_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'.\statistical_analysis\Descriptive Statistics\exported_data\part6_diagram.png')
st.image(image)

"---------"

st.header('Expert request')
"One of the experts wants to know how accurate the transfermarkt site is in estimating the players' prices. Also, recently there has been a problem in the football industry where players are traded for much more than their real value. For this reason, in this section you are asked to compare the distribution of estimated market values of players sold per season, and the actual market value of transfers per season (omitting free transfers)."
'You can check Jupyter notebook for this part in this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/ExperRequest)'

'In the following, you can see normal probability distribution for both real and estimated market value. The difference between the two values is very small compared to the range of changes.'
image = Image.open(r'.\statistical_analysis\ExperRequest\exported_data\fig_all.png')
st.image(image)

'In the following, you can see normal probability distribution for both real and estimated market value in each seasons.'
image = Image.open(r'.\statistical_analysis\ExperRequest\exported_data\fig_merged.png')
st.image(image)

"---------"
st.header('Players Request')
'To find the clubs that need strikers, we first calculated the defense and attack metrics of each club using the following code:'
'You can check Jupyter notebook for this part in this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/PlayerRequest)'

st.code("""
pos_attack_metrics = [ "goals", "assists", ]
pos_attack_weight = [70, 30 ]

neg_attack_metrics = ["minutes_per_goal"]
neg_attack_weight = [20]

pos_defence_metrics = ["clean_sheets" ]
pos_defence_weight = [20 ]
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
""")

'Then we sort all the clubs based on the difference between these two metrics. Clubs with positive difference between attack metric and deffencet metrik are listed in the following.'

table = pd.read_csv('.\statistical_analysis\PlayerRequest\player_request.csv').reset_index(drop=True)
st.dataframe(table)


"---------"

st.header('Coach Request')
"A coach plans to strengthen the team for the next season. For this reason, you are required to find players who have performed very well and at the same time, have a low price."
'You can check Jupyter notebook for this part in this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/ExperRequest)'

st.subheader('Score Metric')
'The performance metric can be different for eac positions. So in this question, prformance metric has defined as following:'

st.code("""
metric_score=[]

for index,record in main_df.iterrows():
    if record['main_position'] in ['Attack','Attack Right Winger','Attack Centre Forward','Attack Left Winger','Attack Second Striker']:
       goal=int(record['Goals'])
       Assist=int(record['Assists'])
       ppg = record['PPG'] # teammate_score
       forward_metric=(3*goal+Assist) + ppg
       metric_score.append(forward_metric)

    elif record['main_position'] =='Goalkeeper':
        clean_sheet=int(record['Clean sheets'])
        ppg = record['PPG'] # teammate_score
        Goalkeeper_metric= (4*clean_sheet)  + ppg
        metric_score.append(Goalkeeper_metric)

    elif record['main_position'] in ['Defender Centre Back','Defender Left Back','Defender Right Back']:
        if math.isnan(record['Clean sheets']):
           clean_sheet=0
        else:
            clean_sheet=int(record['Clean sheets'])   
        red_card=int(record['Red cards'])
        Minutes=int(record['Minutes played'])
        own_goal = record['Own goals']
        ppg = record['PPG'] # teammate_score
        Defender_metric=(4*clean_sheet-red_card)-own_goal + ppg
        if Minutes >= 100:
            increment = Minutes // 100
            Defender_metric += increment+1
        # Assist=int(record['Assists'])
        metric_score.append(Defender_metric)

    elif record['main_position'] in ['midfield','midfield Defensive Midfield','midfield Central Midfield','midfield Attacking Midfield','midfield Left Midfield','midfield Right Midfield']:
        goal=int(record['Goals'])
        red_card=int(record['Red cards'])
        Assist=int(record['Assists'])
        ppg = record['PPG'] # teammate_score
        midfield_metric=((2*goal+3*Assist)-red_card) + ppg
        Minutes=int(record['Minutes played'])
        if Minutes >= 100:
            increment = Minutes // 100
            midfield_metric += increment+1
        metric_score.append(midfield_metric)  

    else:
         metric_score.append(0)    
""")

st.subheader('Selected Players')
'Next we use this metric to rank players, then we find players that have both condition:'

st.code("""
# based on the top 30% performance and the bottom 40% price

# Calculate the cutoff values for performance and price
dl=final_df_sorted.sort_values(by='Score',ascending=False)
performance_cutoff = dl['Score'].quantile(0.7)  # Top 30%
dl=final_df_sorted.sort_values(by='market_value_y',ascending=False)
price_cutoff = dl['market_value_y'].quantile(0.6)  # Bottom 40%

# Create the subsets based on the cutoff values
bottom_price_subset = dl[final_df_sorted['market_value_y'] <= price_cutoff]
dl=final_df_sorted.sort_values(by='Score',ascending=False)
top_performance_subset = dl[final_df_sorted['Score'] >= performance_cutoff]


# Calculate the intersection
intersection_df = final_df_sorted.loc[top_performance_subset.index.intersection(bottom_price_subset.index)]

# Print the intersection
intersection_df
""")

'**Selected Players**: 285 players'
selected_players = pd.read_csv("F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Statistical_Coach'sRequest\exported_data\selected_players.csv")
st.dataframe(selected_players.drop(columns='Unnamed: 0').sort_values(by='Score', ascending=False))

st.subheader('Probability Distribution')

'Now we check our selection by ploting normal prabability distrbutions for both the selected players and the socity:'
image = Image.open(r".\statistical_analysis\Statistical_Coach'sRequest\exported_data\fig3.png")
st.image(image)

image = Image.open(r".\statistical_analysis\Statistical_Coach'sRequest\exported_data\fig1.png")
st.image(image)

image = Image.open(r".\statistical_analysis\Statistical_Coach'sRequest\exported_data\fig2.png")
st.image(image)

'Also we can check these distributions for each position:'
image = Image.open(r".\statistical_analysis\Statistical_Coach'sRequest\exported_data\fig4_merge.png")
st.image(image)

st.subheader('Week players')
'To find the weak players in each league, we select players whose performance score is less than IQR/3. For example, in French premier league, we have:'

st.code("""
q1=champ_France['Score'].quantile(0.25)
q3=champ_France['Score'].quantile(0.75)
print(q1,q3)
IQR=q3-q1
drop_players=champ_France[champ_France['Score']<IQR/3]
""")

'**Drop Players:** 45 players'
table = pd.read_csv(r".\statistical_analysis\Statistical_Coach'sRequest\exported_data\drop_players.csv")
st.dataframe(table)


"---------"

st.header('hypothesis-1 Test')
'In this section, first we need a metric to give each player a performance score. for this section we use following code which is very similar to the metric in section Coach Request.'
'You can see code for this section using this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/hypothesis1)'

st.code("""
metric_score=[]
for index,record in df.iterrows():
    if record['position_group'] == 'Attack':
        Appearances = record['Appearances']
        goal = record['Goals']
        Assist= record['Assists']
        ppg = record['PPG'] # teammate_score
        forward_metric=(3*goal+Assist)/Appearances + ppg 
        Minutes= record['Minutes played']
        if Minutes >= 100:
            increment = Minutes // 100 # experience_score
            forward_metric += increment+1
        metric_score.append(forward_metric)

    elif record['position_group'] =='Goalkeeper':
        clean_sheet= record['player_clean_sheet']
        goal_coneded= record['Goals conceded']
        own_goal = record['Own goals']
        Appearances = record['Appearances']
        ppg = record['PPG'] # teammate_score
        Goalkeeper_metric= (3*clean_sheet - goal_coneded - 2*own_goal)/Appearances + ppg
        Minutes= record['Minutes played']
        if Minutes >= 100:
            increment = Minutes // 100 # experience_score
            Goalkeeper_metric += increment+1
        metric_score.append(Goalkeeper_metric)


    elif record['position_group'] == 'Defender':
        team_cleansheet = record['club_clean_sheet']   
        red_card=int(record['Red cards'])
        Minutes= record['Minutes played']
        own_goal = record['Own goals']
        Appearances = record['Appearances']
        ppg = record['PPG'] # teammate_score
        Defender_metric=(2*team_cleansheet-red_card -own_goal)/Appearances + ppg
        if Minutes >= 100:
            increment = Minutes // 100 # experience_score
            Defender_metric += increment+1
        metric_score.append(Defender_metric)

    elif record['position_group'] == 'midfield':
        goal= record['Goals']
        red_card= record['Red cards']
        Assist= record['Assists']
        Appearances = record['Appearances']
        ppg = record['PPG'] # teammate_score
        midfield_metric=((goal+Assist)*3-red_card)/Appearances + ppg
        Minutes= record['Minutes played']
        if Minutes >= 100:
            increment = Minutes // 100 # experience_score
            midfield_metric += increment+1
        metric_score.append(midfield_metric)    
    else:
         metric_score.append(0)   

df['perf_score'] = metric_score
""")

'By normalizing performance score in each position, using following code, we will have boxplot diagram for performance score.'

st.code("""
df.loc[df[df.position_group == 'Attack'].index, 'perf_score'] = normalize(df[df.position_group == 'Attack'].perf_score)
df.loc[df[df.position_group == 'Goalkeeper'].index, 'perf_score'] = normalize(df[df.position_group == 'Goalkeeper'].perf_score)
df.loc[df[df.position_group == 'Defender'].index, 'perf_score'] = normalize(df[df.position_group == 'Defender'].perf_score)
df.loc[df[df.position_group == 'midfield'].index, 'perf_score'] = normalize(df[df.position_group == 'midfield'].perf_score)
""")

image = Image.open(r".\statistical_analysis\hypothesis1\metric_after_normalization.png")
st.image(image)

'We distinguished each season if it is the first season that players have joind new club by following code:'

st.code("""
result = []
for pid in new_df.player_id.unique().tolist():
    seasons = new_df[new_df.player_id == pid].Season.tolist()
    # print(pid)
    for j, s in enumerate(seasons):
        # print(j, s)
        c_cid = new_df[(new_df.player_id == pid) & (new_df.Season == s)].club_id.values[0]
        if j == 0:
            p_cid = c_cid
        else:
            p_cid = new_df[(new_df.player_id == pid) & (new_df.Season == seasons[j-1])].club_id.values[0]
        
        if c_cid != p_cid:
            result.append({'player_id':pid, 'seasons':seasons[j], 'club_id':c_cid, 'New_season':True})
        else:
            result.append({'player_id':pid, 'seasons':seasons[j], 'club_id':c_cid, 'New_season':False})

status_df = pd.DataFrame(result)
""")

'Finally we split two groups based on players age an run tow-sample t-test. In the followin you can see the result:'
image = Image.open(r".\statistical_analysis\hypothesis1\hypothesis1_result.png")
st.image(image)

'Also we ran this test for each position:'
image = Image.open(r".\statistical_analysis\hypothesis1\hypothesis1_secondary_result.png")
st.image(image)

'**Discuss the results**'
'''
* According to the normal distribution diagram for the two groups, as well as the result of the t-test, there is no significant difference between the two groups.
* However, a more detailed examination of the difference in performance, at least in the first season, shows that the performance of goalkeepers is related to age. It can be interpreted that a goalkeeper needs a lot of agility and increasing age can affect the goalkeeper's performance.
* It was tried to be a metric for each position according to the goals of that group of positions. Therefore, it can be interpreted that in the case of most positions, age should not be considered in evaluating the performance of players at least in the first season
'''

"---------"

st.header('hypothesis-2 Test')
'In this section, we examine the hypothesis that the performance of teams in the European Champions League is better than other teams in the league.'
'You can see code for this section using this [link](https://github.com/MHBehoozi/Transfermarkt/tree/master/statistical_analysis/hypothesis2)'

"We used two metrics for the performance of the clubs. The first is the season's points and the second is the number of clean sheets in the season. In the following, you can see the results of two-sample t-test for both metrics."
image = Image.open(r".\statistical_analysis\hypothesis2\hypothesis2_result.png")
st.image(image)