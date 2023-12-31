import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & BlueBerry Oatmeal')
streamlit.text('🥗 Kale Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Display the table on the page.
streamlit.dataframe(my_fruit_list)
#Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#New Section to display FruitVice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
  else:
    
         back_from_function=get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)
         #streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")


my_data_row = my_cur.fetchall()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
streamlit.header("My fruit load list contains:")
#Snowflake related functions
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         #my_cur.execute("Select * from fruit_load_list")
         #my_cur.execute("insert into fruit_load_list values('from streamlit')")
          my_cur.execute("insert into fruit_load_list values('" +add_my_fruit+"')")
          return "Thanks for adding" + new_fruit
         #return my_cur.fetchall()
add_my_fruit=streamlit.text_input('what fruit would you like to add?')
streamlit.header("View our fruit List-Add your favourites!")
if streamlit.button('Get Fruit List'):
     my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function=insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)
     #my_data_rows=get_fruit_load_list()
     #my_cnx.close()
streamlit.dataframe(my_data_row)
#streamlit.text("what fruit would you like to add?")
#streamlit.text(my_data_row)
add_my_fruit=streamlit.text_input('what fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('test')")
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
#streamlit.stop()
