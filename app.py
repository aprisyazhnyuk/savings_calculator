import streamlit as st
from datetime import date, timedelta
import pandas as pd

# --- Inputs ---
initial_amount = st.number_input("Начальная сумма", value=1000.0)
rate = st.number_input("Годовая ставка (%)", value=15.0)

target_payout = st.number_input(
    "Целевой дневной доход",
    value=5.0
)

# --- Calculations ---
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []

start_date = date.today()

hit_date = None
hit_index = None

day = 0

# --- Simulation until target payout reached + 1 year after ---
while True:
    if day > 0:
        amount *= (1 + daily_rate)

    current_date = start_date + timedelta(days=day)

    daily_payout = amount * daily_rate

    values.append(amount)
    dates.append(current_date)

    # detect hit condition
    if hit_date is None and daily_payout >= target_payout:
        hit_date = current_date
        hit_index = day

    # stop: 1 year after hit
    if hit_date is not None and day >= hit_index + 365:
        break

    day += 1

# --- DataFrame ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

# --- Add marker series (for visual “stripe”) ---
df["Цель достигнута"] = None

if hit_date:
    df.loc[df["Дата"] == hit_date, "Цель достигнута"] = df.loc[df["Дата"] == hit_date, "Баланс"]

# --- Chart ---
st.line_chart(df.set_index("Дата"))

# --- Output info ---
if hit_date:
    st.success(f"Целевой дневной доход достигнут: {hit_date}")
else:
    st.warning("Цель не достигнута в текущем горизонте")
