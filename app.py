import streamlit as st
import datetime

st.title("Savings App")

# Show today's date
today = datetime.date.today()
st.write("Today's date is:", today)

st.header("Input your data")

current_balance = st.number_input(
    "Current balance (RUB):",
    min_value=0.0,
    value=10000.0,
    step=1000.0
)

annual_rate = st.number_input(
    "Annual interest rate (%):",
    min_value=0.0,
    max_value=100.0,
    value=7.0,
    step=0.1
)

target_daily_income = st.number_input(
    "Target daily income (RUB):",
    min_value=0.0,
    value=300.0,
    step=50.0
)

st.header("Your inputs")

st.write("Current balance:", current_balance)
st.write("Annual rate:", annual_rate)
st.write("Target daily income:", target_daily_income)
