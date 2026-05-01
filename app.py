import streamlit as st
from datetime import date, timedelta
import pandas as pd

# --- Inputs ---
initial_amount = st.number_input("Начальная сумма", value=1000.0)
rate = st.number_input("Годовая ставка (%)", value=15.0)

target_amount = st.number_input(
    "Целевая сумма",
    value=initial_amount * 2
)

period_option = st.selectbox(
    "Период",
    ["1 месяц", "3 месяца", "6 месяцев", "1 год"]
)

# --- Period mapping ---
days_map = {
    "1 месяц": 30,
    "3 месяца": 90,
    "6 месяцев": 180,
    "1 год": 365
}
days = days_map[period_option]

# --- Calculations ---
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []

start_date = date.today()

hit_date = None

for day in range(0, days + 1):
    if day > 0:
        amount *= (1 + daily_rate)

    current_date = start_date + timedelta(days=day)

    values.append(amount)
    dates.append(current_date)

    if hit_date is None and amount >= target_amount:
        hit_date = current_date

# --- Build dataframe ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

# --- Add "stripe marker" column ---
df["Цель достигнута"] = None

if hit_date:
    df.loc[df["Дата"] == hit_date, "Цель достигнута"] = target_amount

# --- Chart ---
st.line_chart(df.set_index("Дата"))

# --- Info ---
if hit_date:
    st.success(f"Цель достигнута: {hit_date}")
else:
    st.warning("Цель не достигнута за выбранный период")
