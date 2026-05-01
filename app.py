import streamlit as st
from datetime import date, timedelta
import pandas as pd

# Inputs (in Russian)
initial_amount = st.number_input("Начальная сумма", value=1000.0)
rate = st.number_input("Годовая ставка (%)", value=15.0)

# Preset period selection
period_option = st.selectbox(
    "Период",
    ["1 месяц", "3 месяца", "6 месяцев", "1 год"]
)

# Convert period to days
if period_option == "1 месяц":
    days = 30
elif period_option == "3 месяца":
    days = 90
elif period_option == "6 месяцев":
    days = 180
else:
    days = 365

# Interest calculation
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []

start_date = date.today()

for day in range(days):
    amount *= (1 + daily_rate)
    values.append(amount)
    dates.append(start_date + timedelta(days=day))

# DataFrame with dates
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

df = df.set_index("Дата")

# Plot
st.line_chart(df)
