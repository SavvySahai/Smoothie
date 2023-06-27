# IMPORT ALL THE NECESSARY LIBRARIES REQUIRED
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# ADDING THE TITLE AND HEADERS
st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avacado Toast')

# OPTIONS TO DISPLAY ALL THE FRUIT OPTION TO CHOOSE THE SMOOTHIE
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# PICKING THE FRUITS THEY WANT TO INCLUDE 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# DISPLAYING IN THE TABULAR FORM
# my_fruit_list = my_fruit_list.set_index('Fruit')
st.dataframe(fruits_to_show)

# CREATING FUNCTION FOR FRUITYVICE DATA
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# DISPLAYING THE FRUITYVICE FRUIT ADVICE 
# (NOTE: WE ARE USING THE TRY-EXCEPT BLOCK TO DISPLAYING AN ERROR IF NOTHING IS ENTERED OR IF A THE FRUIT DOESN'T EXIST)
st.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = st.text_input('What fruit information would you like?')
  if not fruit_choice:
      st.error("Please select a fruit to get information!")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      st.dataframe(back_from_function)
      
except URLError as e:
    st.error()

# DISPLAYING OF THE LIST OF FRUITS
st.header("View Our Fruit List - Add Your Favorites!")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()
        
# Add a button to load the fruit        
if st.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)
    
# Adding the fruit by user
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" +  + "')")
        return "Thanks for adding " + new_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    st.text(back_from_function)
