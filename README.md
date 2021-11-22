# Project Title: Fundamentals Stock Dashboard

---

> Author: Amah Martin
> Created: 11-14-2021
> Last Updated:  11-20-2021

## Table of Contents

- Project Summary
- Technical Summary
- Features
- Milestones
- Requirements to Run the Application

## Project Summary

This is a stock dashboard showing basic stock information once a user inputs a stock ticker. Dashboard is created using Streamlit and data is pulled from the IEX Cloud API. Previous called from the API is also stored in memory using Redis.

## Technical Summary

The following main technologies are used to build this application:

- Python 3.8
- Streamlit
- Redis

The there are also modules  used to run this application which can be referenced in the requirements.txt file.

## Features

- Core Features will include the following\:

  1. User will have the ability to enter a valid stock ticker into the dashboard and pull up overview data.
  2. User will have the ability to change the view to another page by selecting an option from the dropdown box in the sidebar.
  3. If stock ticker has been enter before data can be pulled from cached.
  4. As new stock tickers are entered into the input field it will be stored in to in-memory database for a temporary amount of time before expiration

## Milestones

1. Create main view of dashboard
2. Call data from API
3. Store new API calls to in-memory database

## Requirements to Run Application

- Ensure you have Python 3 program downloaded first
- Ensure that you have [Redis](https://redis.io/) installed
  - Instructions on installing Redis on [Mac](https://phoenixnap.com/kb/install-redis-on-mac)
  - Instructions on installing Redis on [Windows](https://redis.com/ebook/appendix-a/a-3-installing-on-windows/a-3-2-installing-redis-on-window/)
- Make a pull request or download the files from the GitHub repository
- You need to make sure you have an IEX Cloud API Key before running the program.
- In terminal navigate to root folder of project
- Create a config.py file and type `API_KEY = "yourapikey"` and save
- In terminal type: `pip install -r requirements.txt` and push enter to download appropriate modules to run program
- Be sure that redis is running before starting the program by typing the following in a Windows Subsystem for Linux or in Linux (ex. Ubuntu) `sudo service redis-server start`
- Once packages are downloaded, in terminal type: `streamlit run stock_dashboard.py` and push enter to run the program
