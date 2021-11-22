import datetime as dt

from requests.api import post

def format_number(number):
    """Formats a number to add commas"""
    return f"{number:,}"


def round_number(number):
    """Takes a number and returns the number as a rounded integer"""
    return f"{round(number,2)}"

def convert_date(date_num):
    """Converts string date to date format"""
    pre_format = "%Y-%m-%d"
    post_format = "%m-%d-%Y"
    converted_dt = dt.datetime.strptime(date_num, pre_format)
    return converted_dt.strftime(post_format)
