import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objects as go

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

while True:
    if day > 0:
        amount *= (1 + daily_rate)

    current_date = start_date + timedelta(days=day)

    daily_payout = amount * daily_rate

    values.append(amount)
    dates.append(current_date)

    if hit_date is None and daily_payout >= target_payout:
        hit_date = current_date
        hit_index = day

    if hit_date is not None and day >= hit_index + 365:
        break

    day += 1

# --- DataFrame ---
df = pd.DataFrame({
    "Дата": dates,
    "Баланс": values
})

# --- Plotly chart ---
fig = go.Figure()

# main balance line
fig.add_trace(go.Scatter(
    x=df["Дата"],
    y=df["Баланс"],
    mode="lines",
    name="Баланс"
))

# target marker point
if hit_date:
    hit_balance = df.loc[df["Дата"] == hit_date, "Баланс"].values[0]

    fig.add_trace(go.Scatter(
        x=[hit_date],
        y=[hit_balance],
        mode="markers",
        name="Цель достигнута",
        marker=dict(size=10, color="blue")
    ))

    # vertical red line (THIS is what you wanted)
    fig.add_vline(
        x=hit_date,
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

# layout
fig.update_layout(
    title="Рост капитала и достижение целевого дохода",
    xaxis_title="Дата",
    yaxis_title="Баланс",
    hovermode="x unified"
)

# --- Render ---
st.plotly_chart(fig, use_container_width=True)

# --- Info ---
if hit_date:
    st.success(f"Целевой дневной доход достигнут: {hit_date}")
else:
    st.warning("Цель не достигнута")
