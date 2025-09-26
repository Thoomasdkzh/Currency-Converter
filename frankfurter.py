from api import get_url
import json
from datetime import datetime, timedelta

BASE_URL = "https://api.frankfurter.dev/v1"

def get_currencies_list():
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the list of available currencies.
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the list of currency codes and return it as Python list.
    Otherwise it will return the value None.

    Parameters
    ----------
    None

    Returns
    -------
    list
        List of available currencies or None in case of error
    """
    url = f"{BASE_URL}/currencies"
    response = get_url(url)
    if response is not None:
        try:
            data = json.loads(response)
            return list(data.keys())
        except Exception:
            return None
    return None
    

def get_latest_rates(from_currency, to_currency, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the latest conversion rate between the provided currencies. 
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the latest conversion rate and the date and return them as 2 separate objects.
    Otherwise it will return the value None twice.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted

    Returns
    -------
    str
        Date of latest FX conversion rate or None in case of error
    float
        Latest FX conversion rate or None in case of error
    """
    url = f"{BASE_URL}/latest?base={from_currency}&symbols={to_currency}"
    response = get_url(url)
    if response is not None:
        try:
            data = json.loads(response)
            date = data.get("date")
            rates = data.get("rates", {})
            rate = rates.get(to_currency)
            return date, rate
        except Exception:
            return None, None
    return None, None

def get_historical_rate(from_currency, to_currency, from_date, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the conversion rate for the given currencies and date
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the conversion rate and return it.
    Otherwise it will return the value None.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted
    from_date : str
        Date when the conversion rate was recorded

    Returns
    -------
    float
        Latest FX conversion rate or None in case of error
    """
    url = f"{BASE_URL}/{from_date}?base={from_currency}&symbols={to_currency}"
    response = get_url(url)
    if response is not None:
        try:
            data = json.loads(response)
            rates = data.get("rates", {})
            rate = rates.get(to_currency)
            return rate
        except Exception:
            return None
    return None
    
def get_rate_trend(from_currency: str, to_currency: str, years: int = 3) -> dict:
    """
    Fetches historical rates for the past N years on a quarterly basis and returns a dictionary with dates as keys and rates as values.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    years : int
        Number of years in the past for which to fetch rates

    Returns
    -------
    dict
        Dictionary containing dates and their corresponding rates
    """
    start_date = (datetime.today().date() - timedelta(days=years * 365))
    url = f"{BASE_URL}/{start_date}..?base={from_currency}&symbols={to_currency}"
    response = get_url(url)
    if response is not None:
        try:
            data = json.loads(response)
            rates = data.get("rates", {})
            return {date: rate[to_currency] for date, rate in rates.items()}
        except Exception:
            return {}
    return {}
    
