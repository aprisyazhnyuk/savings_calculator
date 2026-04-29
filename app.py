import matplotlib
matplotlib.use("Agg")

import datetime
import matplotlib.pyplot as plt
import streamlit as st


def get_user_input():
    current_balance = st.number_input(
        "Текущее состояние накопительного счёта, руб.:",
        min_value=0.0,
        value=10000.0,
        step=1000.0
    )
    annual_rate = st.number_input(
        "Годовая процентная ставка, %:",
        min_value=0.0,
        max_value=100.0,
        value=7.0,
        step=0.1
    )
    target_amount = st.number_input(
        "Желаемый ежедневный доход, руб.:",
        min_value=0.0,
        value=300.0,
        step=50.0
    )
    return current_balance, annual_rate, target_amount


def calculate_daily_growth(current_balance, daily_rate, start_date, end_date):
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


def find_target_threshold(balances, dates, target_amount, daily_rate):
    for balance, date in zip(balances, dates):
        daily_interest = balance * daily_rate
        if daily_interest >= target_amount:
            return date, balance
    return None, None


def plot_growth_chart(dates, balances, threshold_date, threshold_balance):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, balances, label="Рост накоплений")

    if threshold_date and threshold_balance:
        plt.axvline(
            x=threshold_date,
            linestyle="--",
            label=f"Порог достигнут: {threshold_date.strftime('%d.%m.%Y')}"
        )
        plt.axhline(y=threshold_balance, linestyle=":", alpha=0.7)

        plt.annotate(
            f"{threshold_balance:,.0f} руб.",
            xy=(threshold_date, threshold_balance),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", alpha=0.3),
            fontsize=9
        )

    # Format Y axis nicely
    plt.gca().yaxis.set_major_formatter(lambda x, _: f"{x:,.0f}")

    plt.title("Рост накоплений до конца года")
    plt.xlabel("Дата")
    plt.ylabel("Сумма на счёте, руб.")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)


def main():
    st.title("Калькулятор роста накоплений")

    current_balance, annual_rate, target_amount = get_user_input()

    if annual_rate == 0:
        st.error("Процентная ставка должна быть больше 0")
        return

    # Calculate daily rate once
    daily_rate = (annual_rate / 100) / 365

    # Show required balance immediately
    required_balance = target_amount / daily_rate
    st.info(
        f"Необходимый баланс для {target_amount:,.0f} руб./день: "
        f"{required_balance:,.2f} руб."
    )

    st.caption(
        "Примечание: расчёт предполагает ежедневное начисление процентов (сложный процент). "
        "В реальных банковских продуктах условия могут отличаться."
    )

    if st.button("Построить график"):
        today = datetime.date.today()
        end_of_year = datetime.date(today.year, 12, 31)

        dates, balances = calculate_daily_growth(
            current_balance,
            daily_rate,
            today,
            end_of_year
        )

        threshold_date, threshold_balance = find_target_threshold(
            balances,
            dates,
            target_amount,
            daily_rate
        )

        plot_growth_chart(
            dates,
            balances,
            threshold_date,
            threshold_balance
        )

        if threshold_date and threshold_balance:
            st.success(
                f"Сумма накоплений для дохода ≥ {target_amount:,.0f} руб./день: "
                f"**{threshold_balance:,.2f} руб.**"
            )
            st.success(
                f"Дата достижения: **{threshold_date.strftime('%d.%m.%Y')}**"
            )
        else:
            st.warning(
                f"До конца года не будет достигаться ежедневный доход "
                f"в {target_amount:,.0f} руб."
            )


if __name__ == "__main__":
    main()
