import datetime as dt

def format_number(number):
    """Formats a number to add commas"""
    return f"{number:,}"


def round_number(number):
    """Takes a number and returns the number as a rounded integer"""
    return f"{round(number,2)}"

def convert_date(date_num):
    """Converts integer date to date format"""
    format = "%Y-%m-%d"
    return dt.datetime.strptime(date_num, format)
