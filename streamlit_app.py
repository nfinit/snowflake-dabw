import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') # set the index so multiselect will show fruit names

my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
sf_fruit_list = my_cur.fetchall()

streamlit.title('New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.text('Avocado Toast')

streamlit.header('Build Your Own Fruit Smoothie')

# allow user to pick fruits from the list using a streamlit multi-select
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Strawberries','Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# show nutrition information on selected fruits
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruit Advice from Fruityvice!')
try:
    fruit_choice = streamlit.selectbox("Pick a fruit:", list(my_fruit_list.index))
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information!")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # convert JSON to tabular data with pandas
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

streamlit.stop()
streamlit.header('Local fruits')
streamlit.dataframe(sf_fruit_list)
streamlit.text_input('Add a new fruit:')
