
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.coins import market_cap_df
from volatility_weighting.close_to_close import volatilities1
from volatility_weighting.YangZhang import volatilities2

average_volatilities = {coin: volatility.mean() for coin, volatility in volatilities2.items()}
average_volatility_df = pd.DataFrame(list(average_volatilities.items()), columns = ['Symbol', 'Average Volatility']).set_index('Symbol')

inverse_average_volatility = 1 / average_volatility_df['Average Volatility']

weighted_values = np.sqrt(inverse_average_volatility * market_cap_df['Market Cap'])

weights = (weighted_values / weighted_values.sum())
weights_df = pd.DataFrame(weights, columns = ['Weight'])
weights_df_sorted1 = weights_df.sort_values(by = 'Weight', ascending = False)

print(weights_df_sorted1)
