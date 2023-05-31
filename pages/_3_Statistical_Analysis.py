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

part1_table = pd.read_csv(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part1_table.csv')
st.table(part1_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part1_diagram.png')
st.image(image)

'Also you can see similar information for the proportion of players appearances in games in the following'

part1_2_table = pd.read_csv(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part1_2_table.csv')
st.table(part1_2_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part1_2_diagram.png')
st.image(image)

st.subheader('Question 2: The relationship between the number of goals scored and the estimated market value for a player in season 2021/22')

'In this question, after removing outliers, we are going to draw a scatter plot between `players total goals` and `players market value` and try to draw linear regression between them. Parameters of linear regression have been estimatred using `stats.linregress()`'
'As you can see, there is no linear relation between them:'
image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part2_diagram.png')
st.image(image)

st.subheader('Question 3: The relationship between the number of goals scored and the estimated market value for a striker in season 2021/22')

'In this question, after removing outliers, we are going to draw a scatter plot between `strikers total goals` and `strikers market value` and try to draw linear regression between them. Parameters of linear regression have been estimatred using `stats.linregress()`'
'As you can see, there is no linear relation between them:'
image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part3_diagram.png')
st.image(image)

st.subheader('Question 4: Distribution of player estimated market value by position in season 2021/22')

'After removing the outlier data, boxplot digram of estimated market value has been drawn for each position'

image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part4_diagram.png')
st.image(image)

# st.subheader('Question 5: The total number of goals scored in each leagues in season 2021/22')
# 'After removing the outlier data, bar chart of total goals scored has been drawn for each league'

st.subheader('Question 5: Distribution of goals scored in each leagues in season 2021/22')
'After removing the outlier data, the common statistical probability distributions were checked on total goals scored. Python Fitter library has been used for this purpose'

image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part5_diagram.png')
st.image(image)

st.subheader('Question 6: The distribution of the total amount of money that the clubs had to spend to buy players during seasons 2017/18 to 2021/22')
'For this question, first, the total amount of money that the clubs had to spend to buy players in each season has computed. Next, after removing outliers, the common statistical probability distributions were checked on this feature. Python Fitter library has been used for this purpose'

part6_table = pd.read_csv(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part6_table.csv')
st.table(part6_table.rename(columns={'Unnamed: 0':'distribution'}))
image = Image.open(r'F:\Jupyter\Quera Data Science\BootCamp\Projects\Transfermarkt-1\statistical_analysis\Descriptive Statistics\exported_data\part6_diagram.png')
st.image(image)


