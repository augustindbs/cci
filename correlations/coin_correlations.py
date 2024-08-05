
import pandas as pd
import os
import sys
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tkinter import Tk, Label, Button, Listbox, END, MULTIPLE
from data.coins import coins_close
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

for crypto in call['data']:
    symbol = crypto['symbol']
    name = crypto['name']
    
    if name not in stablecoins:
        coins.append(symbol)

manual_overrides = {
    'PEPE': 'PEPE24478-USD',
    'APT': 'APT21794-USD',
    'MNT': 'MNT27075-USD',
    'RENDER': 'RNDR-USD',
    'ARB': 'ARB11841-USD'
}

correlations = coins_close.corr(method = 'pearson')

class CoinSelectorApp:
    
    def __init__(self, root):

        self.root = root
        self.root.title("Coin Selector")
        
        self.label = Label(root, text = "Select Two Coins", font = ('Helvetica', 12), padx = 20)
        self.label.pack(pady = 10)
        
        self.coin_listbox = Listbox(root, selectmode = MULTIPLE, height = 10, width = 30)
        
        for coin in coins:
            self.coin_listbox.insert(END, coin)

        self.coin_listbox.pack(pady = 15, padx = 20)
        
        self.select_button = Button(root, text = "Plot Selected Coins", command = self.plot_coins)
        self.select_button.pack(pady = (0, 10))

        self.heatmap_button = Button(root, text = "View Correlation Heatmap", command = self.plot_heatmap)
        self.heatmap_button.pack(pady = (0, 15))
        

    def plot_coins(self):

        selected_indices = self.coin_listbox.curselection()
        
        selected_coins = [self.coin_listbox.get(i) for i in selected_indices]
        
        coin1, coin2 = selected_coins

        fig, ax1 = plt.subplots(figsize = (16, 12))

        ax1.set_xlabel('Date')
        ax1.set_ylabel(coin1, color = 'tab:blue')
        ax1.plot(coins_close.index, coins_close[coin1], color = 'tab:blue', label = coin1)
        ax1.tick_params(axis = 'y', labelcolor = 'blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel(coin2, color = 'red')
        ax2.plot(coins_close.index, coins_close[coin2], color = 'tab:red', label = coin2)
        ax2.tick_params(axis = 'y', labelcolor = 'tab:red')

        correlation = correlations.loc[coin1, coin2]
        plt.title(f'{coin1} and {coin2} Correlation: {correlation:.2f}', fontsize = 18, color = 'white', pad = 20)
        plt.figtext(0.15, 0.85, f'Correlation: {correlation:.2f}', fontsize = 12, color = 'black', bbox = dict(facecolor = 'white', alpha = 0.8))
        
        plt.show()

    def plot_heatmap(self):

        plt.figure(figsize = (16, 12))
        sns.heatmap(correlations, annot = True, cmap = 'coolwarm', fmt = '.2f', linewidths = 0.5, linecolor = 'white')
        plt.title('Correlation Heatmap of Top 20 Cryptocurrencies (Excluding Stablecoins)', fontsize = 20, color = 'black', pad = 30)
        plt.show()

root = Tk()
app = CoinSelectorApp(root)
root.mainloop()