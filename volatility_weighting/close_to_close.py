
import numpy as np

from data.coins import coins_data

def close_to_close(price_data):

    log_return = (price_data['Close'] / price_data['Close'].shift(1)).apply(np.log)

    squared_log_return = log_return ** 2

    return squared_log_return.dropna()

volatilities1 = {}

for coin, data in coins_data.items():
    volatility = close_to_close(data)
    volatilities1[coin] = volatility

