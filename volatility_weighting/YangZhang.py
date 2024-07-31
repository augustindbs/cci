
import math
import numpy as np
import matplotlib.pyplot as plt

from data.coins import coins_data

def yang_zhang(price_data, window = 30, trading_periods = 365, clean = True):

    log_h = (price_data['High'] / price_data['Open']).apply(np.log)
    log_l = (price_data['Low'] / price_data['Open']).apply(np.log)
    log_c = (price_data['Close'] / price_data['Open']).apply(np.log)
    
    log_oc = (price_data['Open'] / price_data['Close'].shift(1)).apply(np.log)
    log_oc_sq = log_oc ** 2
    
    log_cc = (price_data['Close'] / price_data['Close'].shift(1)).apply(np.log)
    log_cc_sq = log_cc ** 2
    
    rs = log_h * (log_h - log_c) + log_l * (log_l - log_c)
    
    close_vol = log_cc_sq.rolling(
        window = window,
        center = False
    ).sum() * (1.0 / (window - 1.0))
    
    open_vol = log_oc_sq.rolling(
        window = window,
        center = False
    ).sum() * (1.0 / (window - 1.0))
    
    window_rs = rs.rolling(
        window = window,
        center = False
    ).sum() * (1.0 / (window - 1.0))

    k = 0.34 / (1.34 + (window + 1) / (window - 1))
    result = (open_vol + k * close_vol + (1 - k) * window_rs).apply(np.sqrt) * math.sqrt(trading_periods)

    if clean:
        return result.dropna()
    else:
        return result

volatilities2 = {}

for coin, data in coins_data.items():
    volatility = yang_zhang(data)
    volatilities2[coin] = volatility

# for coin, data in coins_data.items():
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 12), sharex = True)

#     ax1.set_title(f'{coin} Price and Yang-Zhang Volatility')
#     ax1.set_ylabel('Price', color='tab:blue')
#     ax1.plot(data.index, data['Close'], label = f'{coin} Price', color = 'tab:blue')
#     ax1.tick_params(axis = 'y', labelcolor = 'tab:blue')
#     ax1.legend(loc = 'upper left')

#     ax2.set_xlabel('Date')
#     ax2.set_ylabel('Volatility', color='tab:red')
#     ax2.plot(volatilities2[coin].index, volatilities2[coin], label = f'{coin} Volatility', color = 'tab:red')
#     ax2.tick_params(axis = 'y', labelcolor = 'tab:red')
#     ax2.legend(loc = 'upper left')

#     fig.tight_layout()
#     fig.add_gridspec()
#     plt.show()

                                                                                                                                                                                                                                                         