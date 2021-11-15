import streamlit as st
import requests
from datetime import timedelta
import config, json, redis
from iex import IEXStock
from helpers import format_number, round_number

redis_client = redis.Redis(host='localhost', port=6379, db=0)

st.title("Fundamental Dashboard")

symbol = st.sidebar.text_input("Symbol", value="MSFT").upper()

stock = IEXStock(config.API_KEY, symbol)

screen = st.sidebar.selectbox(
    "View", ("Overview", "Fundamentals", "News", "Ownership", "Techincals"), index=0)

if screen == "Overview":
    logo_key = f"{symbol}_logo"
    logo = redis_client.get(logo_key)

    if logo is None:
        print("Could not find logo in cache, retrieving from IEX Cloud API")
        logo = stock.get_logo()
        redis_client.set(logo_key, json.dumps(logo))
    else:
        print("Loading logo from cache, serving from redis")
        logo = json.loads(logo)

    company_key = f"{symbol}_company"
    company = redis_client.get(company_key)

    if company is None:
        print("Getting company info from IEX Cloud")
        company = stock.get_company_info()
        redis_client.set(company_key, json.dumps(company))
        redis_client.expire(company_key, timedelta(seconds=10))
    else:
        print("Getting info from cache")
        company = json.loads(company)

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("https://placeimg.com/240/240/any")
        # st.image(logo['url'])

    with col2:
        st.subheader(company['companyName'])
        st.subheader('Description')
        st.write(company['description'])
        st.subheader('Industry')
        st.write(company['industry'])
        st.subheader('CEO')
        st.write(company['CEO'])

if screen == "Fundamentals":
    stats = stock.get_stats()
    st.subheader('Market Cap')
    st.write(format_number(stats['marketcap']))

    st.subheader('PE Ratio')
    st.write(round_number(stats['peRatio']))

    st.subheader('52 Week High')
    st.write(format_number(stats['week52high']))

    st.subheader('52 Week Low')
    st.write(format_number(stats['week52low']))

    st.subheader('TTM Earns Per Share')
    st.write(round_number(stats['ttmEPS']))

    st.subheader('Dividend Yield')
    st.write(round_number(stats['dividendYield']))

    st.subheader('TTM Dividend Rate')
    st.write(round_number(stats['ttmDividendRate']))

    st.subheader('Dividend Yield')
    st.write(round_number(stats['dividendYield']))

    st.subheader('One Month Change Percent')
    st.write(round_number(stats['month1ChangePercent']))

    st.subheader('One Year Change Percent')
    st.write(round_number(stats['year1ChangePercent']))

    st.subheader('Two Year Change Percent')
    st.write(round_number(stats['year2ChangePercent']))

    st.subheader('Five Year Change Percent')
    st.write(round_number(stats['year5ChangePercent']))


if screen == "News":
    pass