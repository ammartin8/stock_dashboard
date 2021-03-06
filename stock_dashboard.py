import streamlit as st
import requests
from datetime import timedelta, datetime
import config, json, redis
from iex import IEXStock
from helpers import format_number, round_number, convert_date

redis_client = redis.Redis(host='localhost', port=6379, db=0)

st.info('Note: The information listed in this dashboard is dummy data.')

st.title("Stock Overview Dashboard")

symbol = st.sidebar.text_input("Symbol", value="MSFT").upper()

stock = IEXStock(config.API_KEY, symbol)

screen = st.sidebar.selectbox(
    "View", ("Overview", "Fundamentals", "News", "Ownership", "Financials"), index=0)

if screen == "Overview":
    # Logo Info
    logo_key = f"{symbol}_logo"
    logo = redis_client.get(logo_key)

    if logo is None:
        print("Could not find logo in cache, retrieving from IEX Cloud API")
        logo = stock.get_logo()
        redis_client.set(logo_key, json.dumps(logo))
    else:
        print("Loading logo from cache, serving from redis")
        logo = json.loads(logo)

    #Company Info
    company_key = f"{symbol}_company"
    company = redis_client.get(company_key)

    if company is None:
        print("Could not find company info in cache, retrieving from IEX Cloud API")
        company = stock.get_company_info()
        redis_client.set(company_key, json.dumps(company))
    else:
        print("Loading company info from cache, serving from redis")
        company = json.loads(company)

    col1, col2 = st.columns([1, 4])

    with col1:
        try:
            st.image(logo['url'])
        except:
            st.image("https://placeimg.com/240/240/tech")


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

    col1, col2 = st.columns([4, 4])

    with col1:
        st.subheader('Market Cap')
        st.write(f"${format_number(stats['marketcap'])}")

        st.subheader('PE Ratio')
        st.write(round_number(stats['peRatio']))

        st.subheader('52 Week High')
        st.write(format_number(stats['week52high']))

        st.subheader('52 Week Low')
        st.write(format_number(stats['week52low']))

        st.subheader('TTM Earns Per Share')
        st.write(round_number(stats['ttmEPS']))
        
    with col2:
        st.subheader('Dividend Yield')
        st.write(round_number(stats['dividendYield']))

        st.subheader('TTM Dividend Rate')
        st.write(round_number(stats['ttmDividendRate']))

        st.subheader('Dividend Yield')
        st.write(round_number(stats['dividendYield']))

        st.subheader('One Month Change Percent')
        st.write(f"{round_number(stats['month1ChangePercent'])}%")

        st.subheader('One Year Change Percent')
        st.write(f"{round_number(stats['year1ChangePercent'])}%")

        st.subheader('Two Year Change Percent')
        st.write(f"{round_number(stats['year2ChangePercent'])}%")

        st.subheader('Five Year Change Percent')
        st.write(f"{round_number(stats['year5ChangePercent'])}%")


if screen == "News":
    news = stock.get_company_news()
    st.subheader('News')

    for article in news:
        try:
            st.image(article['image'])
        except:
            st.image("https://placeimg.com/240/240/tech")
        st.subheader(article['headline'])
        st.write(f"{article['summary']}")
        st.write(f"[Read More]({article['url']})")
        st.write(f"Source: {article['source']}")
        
        if article['hasPaywall'] == True:
            st.write("Paywall Article")
        else:
            st.write("Free Article")
        st.markdown("***")


if screen == "Ownership":
    ownership_info = stock.get_institutional_ownership()

    st.subheader('Institutional Ownership')

    c = st.container()

    for inst_owner in ownership_info: 
        with c:
            st.write(f"**Entity Owner:** {inst_owner['entityProperName']}")
            st.write(f"**Adjusted Holding:** {format_number(inst_owner['adjHolding'])}")
            st.write(f"**Reported Holding:** {format_number(inst_owner['reportedHolding'])}")
            st.write(f"**Filing Date:** {convert_date(inst_owner['filingDate'])}")
            st.markdown("***")


if screen == "Financials":
    balance_sht_data = stock.get_balance_sheet()
    income_stmt_data = stock.get_income_stmt()
    cash_flow_data = stock.get_cash_flow()
    
    with st.expander("Balance Sheet"):
        st.write(f"**Fiscal Year:** {balance_sht_data['balancesheet'][0]['fiscalYear']}")
        st.write(f"**Fiscal Date:** {convert_date(balance_sht_data['balancesheet'][0]['fiscalDate'])}")
        st.write(f"**Report Date:** {convert_date(balance_sht_data['balancesheet'][0]['reportDate'])}")
        st.write(f"**Current Assets:** ${format_number(balance_sht_data['balancesheet'][0]['currentAssets'])}")
        st.write(f"**Current Cash:** ${format_number(balance_sht_data['balancesheet'][0]['currentCash'])}")
        st.write(f"**Long Term Debt:** ${format_number(balance_sht_data['balancesheet'][0]['longTermDebt'])}")
        st.write(f"**Total Assets:** ${format_number(balance_sht_data['balancesheet'][0]['totalAssets'])}")
        st.write(f"**Total Current Liabilities:** ${format_number(balance_sht_data['balancesheet'][0]['totalCurrentLiabilities'])}")
        st.write(f"**Total Liabilities:** ${format_number(balance_sht_data['balancesheet'][0]['totalLiabilities'])}")
        
    with st.expander("Income Statement"):
        st.write(f"**Fiscal Year:** {income_stmt_data['income'][0]['fiscalYear']}")
        st.write(f"**Fiscal Date:** {convert_date(income_stmt_data['income'][0]['fiscalDate'])}")
        st.write(f"**Report Date:** {convert_date(income_stmt_data['income'][0]['reportDate'])}")
        st.write(f"**Total Revenue:** ${format_number(income_stmt_data['income'][0]['totalRevenue'])}")
        st.write(f"**Cost of Revenue:** ${format_number(income_stmt_data['income'][0]['costOfRevenue'])}")
        st.write(f"**EBIT:** ${format_number(income_stmt_data['income'][0]['ebit'])}")
        st.write(f"**Interest Income:** ${format_number(income_stmt_data['income'][0]['interestIncome'])}")
        st.write(f"**Pretax Income:** ${format_number(income_stmt_data['income'][0]['pretaxIncome'])}")
        st.write(f"**Income Tax:** ${format_number(income_stmt_data['income'][0]['incomeTax'])}")
        st.write(f"**Net Income:** ${format_number(income_stmt_data['income'][0]['netIncome'])}")

    with st.expander("Cash Flow Statement"):
        st.write(f"**Fiscal Year:** {cash_flow_data['cashflow'][0]['fiscalYear']}")
        st.write(f"**Fiscal Date:** {convert_date(cash_flow_data['cashflow'][0]['fiscalDate'])}")
        st.write(f"**Report Date:** {convert_date(cash_flow_data['cashflow'][0]['reportDate'])}")
        st.write(f"**Cash Flow:** ${format_number(cash_flow_data['cashflow'][0]['cashFlow'])}")
        st.write(f"**Dividends Paid:** {format_number(cash_flow_data['cashflow'][0]['dividendsPaid'])}")
        st.write(f"**Capital Expenditures:** ${format_number(cash_flow_data['cashflow'][0]['capitalExpenditures'])}")
        st.write(f"**Net Borrowings:** ${format_number(cash_flow_data['cashflow'][0]['netBorrowings'])}")
        st.write(f"**Cash Flow Financing:** ${format_number(cash_flow_data['cashflow'][0]['cashFlowFinancing'])}")
        st.write(f"**Total Investing Cash Flows:** ${format_number(cash_flow_data['cashflow'][0]['totalInvestingCashFlows'])}")


