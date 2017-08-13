from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import quandl as qdl
import requests
import datetime

#qdl.ApiConfig.api_key = "KEY-HERE"

def get_soup(url):
	"""
	Turn URL into a Beautiful Soup object
	"""
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "lxml")
	return soup

def get_sp_list():
    """
    Gets all tickers from S&P 500
    """
    bs = get_soup('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp_companies = bs.find_all('a', class_="external text")
    return sp_companies

def get_dow_list():
    """
    Gets all tickers from DOW30
    """
    bs = get_soup('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
    dow_companies = bs.find_all('a', class_="external text")
    return dow_companies

def get_from_symbol(symbol, **kwargs):
    df = qdl.get('WIKI/{}'.format(symbol), **kwargs)
    df['GOING_UP'] = 0
    for i in range(1, len(df)):
        if df['Adj. Close'].values[i] > df['Adj. Close'].values[i-1]:
            df['GOING_UP'].values[i] = 1
    return df


def get_dataset():
	dataset = {}
	dow_tickers = [i.text for n, i in enumerate(get_dow_list()) if n < 31 and len(i.text) <= 5]
	sp_tickers = [i.text for n, i in enumerate(get_sp_list()) if n%2==0 and len(i.text) <= 5 and '.' not in i]
	for symbol in dow_tickers:
		try:
			print(symbol)
			dataset[symbol] = get_from_symbol(symbol,collapse='daily', start_date='2015-01-01')
		except:
			print('FAIL')
	return dataset