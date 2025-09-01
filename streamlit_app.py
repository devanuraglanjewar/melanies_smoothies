# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custome smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    "Choose up to five ingredients",
    smoothiefroot_response,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for choosen_fruit in ingredients_list:
      ingredients_string += fruit_chosen + ' '
      st.subheader(fruit_chosen + 'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
      sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER) 
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
