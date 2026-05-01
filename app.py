import streamlit as st
from datetime import date, timedelta
import pandas as pd
import altair as alt

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
days = {
    "1 месяц": 30,
    "3 месяца": 90,
    "6 месяцев": 180,
    "1 год": 365
}[period_option]

# --- Calculations ---
daily_rate = rate / 100 / 365

amount = initial_amount
values = []
dates = []

start_date = date.today()

values.append(amount)
dates.append(start_date)

hit_date = None

for day in range(1, days + 1):
    amount *= (1 + daily_rate)

    current_date = start_date + timedelta(days=day)

    values.append(amount)
    dates.append(current_date)

    if hit_date is None and amount >= target_amount:
        hit_date = current_date

# --- Data ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

# --- Base line ---
line = alt.Chart(df).mark_line().encode(
    x="Дата:T",
    y="Баланс:Q"
)

# --- Vertical dashed target line ---
rule = None
if hit_date:
    rule = alt.Chart(pd.DataFrame({"Дата": [hit_date]})).mark_rule(
        strokeDash=[6, 4],
        color="red"
    ).encode(
        x="Дата:T"
    )

chart = line + (rule if rule is not None else 0)

st.altair_chart(chart, use_container_width=True)

# --- Info ---
if hit_date:
    st.success(f"Цель достигнута: {hit_date}")
else:
    st.warning("Цель не достигнута за выбранный период")
