import streamlit as st
from datetime import date


from frankfurter import get_currencies_list, get_latest_rates, get_historical_rate
from currency import reverse_rate, round_rate, format_output
# Display Streamlit App Title

# Get the list of available currencies from Frankfurter

# If the list of available currencies is None, display an error message in Streamlit App

# Add input fields for capturing amount, from and to currencies

# Add a button to get and display the latest rate for selected currencies and amount

# Add a date selector (calendar)

# Add a button to get and display the historical rate for selected date, currencies and amount
st.title("Currency Converter 💱")

# Get the list of available currencies
currencies = get_currencies_list()

if currencies is None:
    st.error("Error fetching currencies from Frankfurter API.")
else:
    # -----------------------
    # User Inputs
    # -----------------------
    amount = st.number_input("Enter the amount to convert:", min_value=0.0, value=1.0, step=1.0)
    from_currency = st.selectbox("From Currency:", options=currencies, index=currencies.index("USD") if "USD" in currencies else 0)
    to_currency = st.selectbox("To Currency:", options=currencies, index=currencies.index("EUR") if "EUR" in currencies else 0)

    # -----------------------
    # Latest Rate Button
    # -----------------------
    if st.button("Get Latest Rate"):
        date_str, rate = get_latest_rates(from_currency, to_currency, amount)
        if date_str is not None and rate is not None:
            st.success(format_output(date_str, from_currency, to_currency, rate, amount))
        else:
            st.error("Error fetching latest rate from Frankfurter API.")

    # -----------------------
    # Historical Rate
    # -----------------------
    selected_date = st.date_input("Select a date for historical rate:", max_value=date.today())

    if st.button("Get Historical Rate"):
        rate = get_historical_rate(from_currency, to_currency, selected_date.strftime("%Y-%m-%d"), amount)
        if rate is not None:
            st.success(format_output(selected_date.strftime("%Y-%m-%d"), from_currency, to_currency, rate, amount))
        else:
            st.error("Error fetching historical rate from Frankfurter API.")









