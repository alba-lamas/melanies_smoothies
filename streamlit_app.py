# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Custumize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

title = st.text_input("Name of smoothie:")
st.write("The name of smoothie will be: ", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)

import streamlit as st

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe, max_selections=5
)
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    for fruit_chosen in ingredients_list:
        st.subheader(fruit_chosen + 'Nutritional Information')
        fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width=True)

    if(st.button("Submin Order")) and ingredients_string:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + title + """')"""    
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

