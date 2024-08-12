
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.coins import coins_close

daily_returns_df = coins_close.pct_change()
daily_returns_df = daily_returns_df.replace([np.inf, -np.inf], np.nan).dropna()

near_zero_threshold = 0.001

def calculate_near_zero_return_frequency(returns_df, threshold):
    near_zero_return_freq = {}

    for coin in returns_df.columns:
        returns = returns_df[coin]
        near_zero_count = ((returns >= -threshold) & (returns <= threshold)).sum()
        total_count = returns.count()
        near_zero_return_freq[coin] = (near_zero_count / total_count) * 100

    return pd.DataFrame.from_dict(near_zero_return_freq, orient = 'index', columns = ['Near Zero Return Frequency'])

near_zero_returns_df = calculate_near_zero_return_frequency(daily_returns_df, near_zero_threshold)