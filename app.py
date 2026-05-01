import streamlit as st
from datetime import date

st.title("My First Finance App")

# Show today's date
today = date.today()
st.write("Today's date is:", today)

# User input
initial_amount = st.number_input(
    "Enter your starting amount:",
    min_value=0.0,
    value=1000.0,
    step=100.0
)

st.write("Your starting amount is:", initial_amount)
