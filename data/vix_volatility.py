
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.coins import coins_close

log_returns = np.log(coins_close / coins_close.shift(1))

rolling_volatility = log_returns.rolling(window = 30).std()

trading_days = 365
annualized_volatility = rolling_volatility * np.sqrt(trading_days)

plt.figure(figsize = (20, 16))

for coin in annualized_volatility.columns:
    plt.plot(annualized_volatility.index, annualized_volatility[coin], label = coin)

plt.title('VIX-like Volatility Index for Cryptocurrencies')
plt.xlabel('Date')
plt.ylabel('Annualized Volatility')
plt.legend()

plt.show()
