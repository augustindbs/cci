
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.coins import market_cap_df
from consistent_returns.memecoins import near_zero_returns_df

inverse_near_zero = 1 / near_zero_returns_df

weighted_values = np.sqrt(market_cap_df['Market Cap'] * inverse_near_zero['Near Zero Return Frequency'])

weights = (weighted_values / weighted_values.sum())
weights_df = pd.DataFrame(weights, columns = ['Weight'])
weights_df_sorted2 = weights_df.sort_values(by = 'Weight', ascending = False)

print(weights_df_sorted2)