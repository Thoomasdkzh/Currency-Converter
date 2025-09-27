import streamlit as st
from datetime import date
import pandas as pd

from frankfurter import get_currencies_list, get_latest_rates, get_historical_rate, get_rate_trend
from currency import format_output

# -----------------------
# App Title 
# -----------------------
st.title("FX Converter")

# -----------------------
# Get the list of currencies
# -----------------------
currencies = get_currencies_list()

if currencies is None:
    st.error("Error fetching currencies from Frankfurter API.")
else:
    # -----------------------
    # User Inputs
    # -----------------------
    st.subheader("🔢 Conversion Inputs")
    amount = st.number_input("Enter the amount to convert:", min_value=0.0, value=1.0, step=1.0)
    from_currency = st.selectbox("From Currency:", options=currencies, index=currencies.index("USD") if "USD" in currencies else 0)
    to_currency = st.selectbox("To Currency:", options=currencies, index=currencies.index("EUR") if "EUR" in currencies else 0)

    if from_currency == to_currency:
        st.warning("⚠️ Please select two different currencies.")

    # -----------------------
    # Latest Rate
    # -----------------------
    if st.button("Get Latest Rate"):
        if from_currency == to_currency:
            st.error("⚠️ Cannot fetch latest rate for the same currency.")
        else:
            date_str, rate = get_latest_rates(from_currency, to_currency, amount)
            if date_str is not None and rate is not None:
                st.success(format_output(date_str, from_currency, to_currency, rate, amount))
            else:
                st.error("Error fetching latest rate from Frankfurter API.")
    
    # -----------------------
    # Rate Evolution Graph
    # -----------------------
    st.subheader("📈 Rate Evolution Over Time")
    years = st.slider("Select number of years to display:", min_value=1, max_value=10, value=3, step=1)

    show_graph = st.checkbox("Show Rate Evolution")
    if show_graph:
        if from_currency == to_currency:
            st.error("⚠️ Cannot show graph for the same currency.")
        else:
            st.subheader(f"📈 Rate Trend Over the Last {years} years")
            trend_data = get_rate_trend(from_currency, to_currency, years)
            if trend_data:
                df = pd.DataFrame(list(trend_data.items()), columns=["Date", "Rate"])
                df["Date"] = pd.to_datetime(df["Date"])
                df = df.sort_values("Date")
                st.line_chart(df.set_index("Date")["Rate"])
            else:
                st.warning("Could not fetch trend data for the selected currencies.")

    # -----------------------
    # Historical Rate
    # -----------------------
    st.subheader("📅 Get Historical Rate")
    selected_date = st.date_input("Select a date for historical rate:", max_value=date.today())

    if st.button("Get Historical Rate"):
        if from_currency == to_currency:
            st.error("⚠️ Cannot fetch historical rate for the same currency.")
        else:
            rate = get_historical_rate(from_currency, to_currency, selected_date.strftime("%Y-%m-%d"), amount)
            if rate is not None:
                st.success(format_output(selected_date.strftime("%Y-%m-%d"), from_currency, to_currency, rate, amount))
            else:
                st.error("Error fetching historical rate from Frankfurter API.")
