
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import yfinance as yf

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

parameters = {
    'start': '1',
    'limit': '23',
    'convert': 'USD'
}

response = requests.get(url, headers = headers, params = parameters)
call = response.json()

stablecoins = {'Tether USDt', 'USDC', 'Dai', 'FDUSD', 'USDD'}

coins = []
market_caps = []

manual_overrides = {
    'PEPE': 'PEPE24478-USD',
    'APT': 'APT21794-USD',
    'MNT': 'MNT27075-USD',
    'RENDER': 'RNDR-USD',
    'ARB': 'ARB11841-USD'
}

for crypto in call['data']:
    symbol = crypto['symbol']
    name = crypto['name']
    market_cap = crypto['quote']['USD']['market_cap']
    
    if name not in stablecoins:
        coins.append(symbol)
        market_caps.append(market_cap)


prices_df = pd.DataFrame()


market_cap_df = pd.DataFrame({
    'Symbol': coins,
    'Market Cap': market_caps
}).set_index('Symbol')


period = 'max'


coins_data = {}

for coin in coins:
    if coin in manual_overrides:
        yf_symbol = manual_overrides[coin]
    else:
        yf_symbol = coin + '-USD'
    
    try:
        price_data = yf.download(yf_symbol, period = period, interval = '1d')

        coins_data[coin] = price_data[['Open', 'High', 'Low', 'Close']]
    
    except Exception as e:
        print(f"Error fetching data for {coin}: {e}")


coins_close = pd.DataFrame()

for coin in coins:
    if coin in manual_overrides:
        yf_symbol = manual_overrides[coin]
    else:
        yf_symbol = coin + '-USD'
    
    try:
        coin_close = yf.download(yf_symbol, period = period, interval = '1d')
        if coin_close.empty:
            print(f"No data for {yf_symbol}. Skipping.")
            
            continue

        coins_close[coin] = coin_close['Close']
   
    except Exception as e:
        print(f"Error fetching data for {yf_symbol}: {e}. Skipping.")