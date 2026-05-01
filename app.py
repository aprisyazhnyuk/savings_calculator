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

# --- Calculations ---
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []

start_date = date.today()

hit_date = None
hit_index = None

day = 0

# --- Simulate until target is reached ---
while True:
    if day > 0:
        amount *= (1 + daily_rate)

    current_date = start_date + timedelta(days=day)

    values.append(amount)
    dates.append(current_date)

    if hit_date is None and amount >= target_amount:
        hit_date = current_date
        hit_index = day

    # stop condition: reached target AND added 1 year after
    if hit_date is not None and day >= hit_index + 365:
        break

    day += 1

# --- DataFrame ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

# --- Target marker column (fake vertical spike) ---
df["Цель достигнута"] = None

if hit_date:
    df.loc[df["Дата"] == hit_date, "Цель достигнута"] = target_amount

# --- Chart ---
st.line_chart(df.set_index("Дата"))

# --- Info ---
if hit_date:
    st.success(f"Цель достигнута: {hit_date}")
else:
    st.warning("Цель не достигнута в разумном горизонте")
