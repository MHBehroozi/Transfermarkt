import streamlit as st


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

st.code("""


""",
    language="python")