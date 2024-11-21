# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session #not in snowflake adjustment
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("My Parents New Healthy Diner :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)





#option = st.selectbox(
 #   "fruit?",
  #  ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Fave fruit = ", option)
name_on_order=st.text_input('Name of Smoothie')
st.write('The name on your smoothie will be:', name_on_order)
cnx=st.connection('snowflake')
session = cnx.session()#get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop() #temp

ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)
if ingredients_list: # checks if null
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        #SEARCH_ON
        #st.text(smoothiefroot_response.json() )
        sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

    time_to_insert=st.button('Submit Order')

    #sql
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values(' """+ingredients_string+"""','"""+name_on_order+ """')"""
  #  +"""')""" # no semicolon?
    #st.write(my_insert_stmt)
    #st.stop() #temp
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")


