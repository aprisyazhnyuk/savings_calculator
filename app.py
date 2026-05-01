import streamlit as st
from datetime import date
import pandas as pd

st.title("Savings Growth Simulator")

st.write("Today's date:", date.today())

initial_amount = st.number_input("Starting amount", value=1000.0)
rate = st.number_input("Annual interest rate (%)", value=15.0)
days = st.slider("Days to simulate", 1, 365, 30)

daily_rate = rate / 100 / 365

amount = initial_amount
values = []

for day in range(days):
    amount *= (1 + daily_rate)
    values.append(amount)

df = pd.DataFrame({
    "Day": range(1, days + 1),
    "Balance": values
})

st.line_chart(df.set_index("Day"))
