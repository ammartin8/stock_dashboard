import requests

class IEXStock:

    def __init__(self, token, symbol):
        self.BASE_URL = "https://sandbox.iexapis.com/stable"
        self.token = token
        self.symbol = symbol

    def get_logo(self):
        """Makes an API call and returns logo image based on user input"""
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)
        
        return r.json()


    def get_company_info(self):
        """Makes an API call and returns specific company information"""
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r =  requests.get(url)
        
        return r.json()

    def get_company_news(self, last=10):
        """Makes an API call and returns last ten company new articles"""
        url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)

        return r.json()


    def get_stats(self):
        """Makes an API Call and returns specific stats information"""
        url = f"{self.BASE_URL}/stock/{self.symbol}/stats/{{stat}}?token={self.token}"
        r =  requests.get(url)
        
        return r.json()
    
    # def get_fundamentals(self, period='quarterly', last=4):
    #     url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
    #     r = requests.get(url)

    #     return r.json()

    def get_institutional_ownership(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_income_stmt(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/income?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_balance_sheet(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/balance-sheet?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_cash_flow(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/cash-flow?token={self.token}"
        r = requests.get(url)

        return r.json()