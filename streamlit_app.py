import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

#st.title("Trying the module")
#st.header('First Line')
#st.text('Hopefully this has displayed without an error.')
#st.text('Using streamlit is really easy.')
#st.text('And if I am stuck I can always refer the docs!')

st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avacado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# my_fruit_list = my_fruit_list.set_index('Fruit')
st.dataframe(fruits_to_show)

#To display the api response
st.header("Fruityvice Fruit Advice!")
# adding a text-box
fruit_choice = st.text_input('What fruit information would you like', 'Kiwi')
st.write('The user entered: ', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# Make this look better
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#puts it in a dataframe as in a table
st.dataframe(fruityvice_normalized)
st.stop()


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains")
st.dataframe(my_data_rows)

# adding a text-box
add_fruit = st.text_input('What fruit would you like to add', 'Rambhutan')
st.write('Thanks for adding ', add_fruit)

my_cur.execute("insert into fruit_load_list values ('test')");
