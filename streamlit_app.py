import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') # set the index so multiselect will show fruit names

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
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
try:
    fruit_choice = streamlit.selectbox("Pick a fruit:", list(my_fruit_list.index))
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information!")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()

streamlit.header('Local fruits')

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()

if streamlit.button('Get fruits now'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
