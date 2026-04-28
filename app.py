import datetime
import matplotlib.pyplot as plt
import streamlit as st

def get_user_input():
    current_balance = st.number_input("Текущее состояние накопительного счёта, руб.:", min_value=0.0, value=10000.0)
    annual_rate = st.number_input("Годовая процентная ставка, %:", min_value=0.0, max_value=100.0, value=7.0)
    target_amount = st.number_input("Желаемая сумма ежедневного дохода, руб.:", min_value=0.0, value=300.0)
    return current_balance, annual_rate, target_amount


def calculate_daily_growth(current_balance: float, annual_rate: float, start_date: datetime.date, end_date: datetime.date) -> tuple[list[datetime.date], list[float]]:
    daily_rate = (annual_rate / 100) / 365
    current_date = start_date
    dates = []
    balances = []
    balance = current_balance

    while current_date <= end_date:
        dates.append(current_date)
        balances.append(balance)
        daily_interest = balance * daily_rate
        balance += daily_interest
        current_date += datetime.timedelta(days=1)

    return dates, balances

def find_target_threshold(balances: list[float], dates: list[datetime.date], target_amount: float, daily_rate: float) -> tuple[datetime.date | None, float | None]:
    for balance, date in zip(balances, dates):
        daily_interest = balance * daily_rate
        if daily_interest >= target_amount:
            return date, balance
    return None, None

def plot_growth_chart(dates: list[datetime.date], balances: list[float], threshold_date: datetime.date | None, threshold_balance: float | None) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(dates, balances, label="Рост накоплений", color="blue")

    if threshold_date and threshold_balance:
        plt.axvline(x=threshold_date, color="red", linestyle="--", label=f"Порог достигнут: {threshold_date.strftime('%d.%m.%Y')}")
        plt.axhline(y=threshold_balance, color="red", linestyle=":", alpha=0.7)
        plt.annotate(f"{threshold_balance:.2f} руб.", xy=(threshold_date, threshold_balance), xytext=(10, 10), textcoords="offset points", bbox=dict(boxstyle="round,pad=0.3", facecolor="red", alpha=0.3), fontsize=9, color="darkred")


    plt.title("Рост накоплений до конца года")
    plt.xlabel("Дата")
    plt.ylabel("Сумма на счёте, руб.")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)  # Вместо plt.show()

def main():
    st.title("Калькулятор роста накоплений")
    current_balance, annual_rate, target_amount = get_user_input()
    if st.button("Построить график"):
        today = datetime.date.today()
        end_of_year = datetime.date(today.year, 12, 31)
        dates, balances = calculate_daily_growth(current_balance, annual_rate, today, end_of_year)
        daily_rate = (annual_rate / 100) / 365
        threshold_date, threshold_balance = find_target_threshold(balances, dates, target_amount, daily_rate)
        plot_growth_chart(dates, balances, threshold_date, threshold_balance)
        if threshold_date and threshold_balance:
            st.success(f"Сумма накоплений для дохода ≥ {target_amount} руб./день: **{threshold_balance:.2f} руб.**")
            st.success(f"Дата достижения: **{threshold_date.strftime('%d.%m.%Y')}**")
        else:
            st.warning("До конца года не будет достигаться ежедневный доход в {target_amount} руб.")

if __name__ == "__main__":
    main()