import streamlit as st
from datetime import date, timedelta
import pandas as pd

# --- Inputs (Russian UI) ---
initial_amount = st.number_input("Начальная сумма", value=1000.0)
rate = st.number_input("Годовая ставка (%)", value=15.0)

period_option = st.selectbox(
    "Период",
    ["1 месяц", "3 месяца", "6 месяцев", "1 год"]
)

# --- Period mapping ---
if period_option == "1 месяц":
    days = 30
elif period_option == "3 месяца":
    days = 90
elif period_option == "6 месяцев":
    days = 180
else:
    days = 365

# --- Calculations ---
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []
daily_payouts = []

start_date = date.today()

for day in range(days):
    payout = amount * daily_rate  # daily profit
    amount += payout              # reinvest

    current_date = start_date + timedelta(days=day)

    # Format date in Russian style (DD.MM.YYYY)
    formatted_date = current_date.strftime("%d.%m.%Y")

    values.append(amount)
    daily_payouts.append(payout)
    dates.append(formatted_date)

# --- Data ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values,
    "Ежедневный доход": daily_payouts
})

df = df.set_index("Дата")

# --- Chart ---
st.line_chart(df["Баланс"])

# --- Optional: show payouts table ---
with st.expander("Показать ежедневные выплаты"):
    st.dataframe(df)
