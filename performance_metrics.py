
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.coins import coins_close, coins_data
from volatility_weighting.weights import weights_df_sorted1
from consistent_returns.weights import weights_df_sorted2

# CHECK FOR NORMALITY IN DAILY RETURNS BEFORE COMPUTING PORTFOLIO METRICS

daily_returns_df = coins_close.pct_change().dropna()
daily_returns_df = daily_returns_df.replace([np.inf, -np.inf], np.nan).dropna()

log_returns_df = np.log(coins_close/coins_close.shift(1))
log_returns_df = log_returns_df.dropna()

fig, axes = plt.subplots(4, 5, figsize = (20, 14))
axes = axes.flatten()

normality_results = {}

for i, coin in enumerate(daily_returns_df.columns):
    ax = axes[i]
    data = daily_returns_df[coin].dropna()

    ax.hist(data, bins = 100, alpha = 0.7, color = 'blue')
    ax.set_title(coin, fontsize = 10)
    ax.set_xlabel('Daily Returns')
    ax.set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# COMPUTING PORTFOLIO RETURNS USING WEIGHTS FROM BOTH APPROACHES

weights_volatility = weights_df_sorted1.loc[daily_returns_df.columns]
weights_near_zero = weights_df_sorted2.loc[daily_returns_df.columns]

portfolio_daily_returns_volatility = (daily_returns_df * weights_volatility['Weight']).sum(axis = 1)
portfolio_daily_returns_near_zero = (daily_returns_df * weights_near_zero['Weight']).sum(axis = 1)

# CALCULATING THE SHARPE RATIO FOR BOTH PORTFOLIOS

def sharpe_ratio(daily_returns, rfr, trading_days):

    mean_daily_returns = daily_returns.mean()
    std_daily_returns = daily_returns.std()

    annualized_return = mean_daily_returns * trading_days
    annualized_std = std_daily_returns * np.sqrt(trading_days)

    sharpe = (annualized_return - rfr) / annualized_std

    return sharpe

sharpe_ratio_volatility = sharpe_ratio(portfolio_daily_returns_volatility, 0.04, 365)
sharpe_ratio_near_zero = sharpe_ratio(portfolio_daily_returns_near_zero, 0.04, 365)

# COMPUTING VaR FOR BOTH PORTFOLIOS

portfolio_log_returns_volatility = (log_returns_df * weights_volatility['Weight']).sum(axis = 1)
portfolio_log_returns_near_zero = (log_returns_df * weights_near_zero['Weight']).sum(axis = 1)

def get_range_returns(historical_returns, days):

    range_returns = historical_returns.rolling(window = days).sum()
    range_returns = range_returns.dropna()

    return range_returns

def value_at_risk(range_returns_df, confidence_interval):
    
    var = -np.percentile(range_returns_df, 100 - (confidence_interval * 100))

    return var

# Example: 5-day VaR for both portfolios with 95% CI

confidence_interval = 0.95
days = 5

var_volatility = value_at_risk(get_range_returns(portfolio_log_returns_volatility, days), confidence_interval)
var_near_zero = value_at_risk(get_range_returns(portfolio_log_returns_near_zero, days), confidence_interval)

print(f"{days}-day VaR (Volatility Weighted, {confidence_interval * 100}% CI): {var_volatility * 100:.2f}%")
print(f"{days}-day VaR (Near Zero Weighted, {confidence_interval * 100}% CI): {var_near_zero * 100:.2f}%")




