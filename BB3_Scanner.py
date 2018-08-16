import tuotrading as tt 
from datetime import date, timedelta
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def bb3_backtest(spread_name, threshold, base_dir, start_date, end_date):
	data = tt.calculate_PnL(spread_name, base_dir, threshold=threshold)
	data.to_csv('test.csv')

	# Calculate daily PnL
	daily_PnL = data.groupby(data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
	daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)

	# Calculate Sharpe Ratio between start and end date:
	temp = daily_PnL.loc[start_date:end_date]['PnL'].copy()
	sharpeRatio = temp.mean() / temp.std() * np.sqrt(len(temp))

	# Calculate drawdown
	daily_PnL['MaxProfit'] = df['cumPnL'].cummax()
	

	return sharpeRatio

def bb3_backtest_delta_days(spread_name, threshold, base_dir, end_date, delta_days):
	start_date = end_date - timedelta(days=delta_days)
	sharpeRatio = bb3_backtest(spread_name, threshold, base_dir, start_date, end_date)
	return sharpeRatio


def bb3_scanner(BB3_list_filename, base_dir, start_date, end_date):
	result = {}
	BB3_list = pd.read_csv(BB3_list_filename, index_col='BB3_name')

	for row in BB3_list.itertuples():
		spread_name = row[0]
		Threshold = row[1]
		
		sharpeRatio = bb3_backtest(spread_name, Threshold, base_dir, start_date, end_date)

		result[spread_name] = sharpeRatio

		print spread_name, sharpeRatio

	df_Sharpe = pd.DataFrame.from_dict({'Sharpe':result}).sort_values(by='Sharpe', ascending=False)

	return df_Sharpe

def bb3_scanner_delta_days(BB3_list_filename, end_date, base_dir):
	start_date = end_date - timedelta(days=delta_days)
	df_Sharpe = bb3_scanner(bb)

def main():
	BB3_list_filename = 'data/BB3_list.csv'
	start_date = date(2018,7,1)
	end_date = date.today()
	base_dir = 'data/data_2018'
	print bb3_scanner(BB3_list_filename, base_dir, start_date, end_date)

def main_2():
	spread_name = 'NKD+ZN'
	threshold = 30
	start_date = date(2018,7,1)
	end_date = date.today()
	delta_days = 60
	base_dir = 'data/data_2018'
	print bb3_backtest(spread_name, threshold, base_dir, start_date, end_date)
	print bb3_backtest_delta_days(spread_name, threshold, base_dir, end_date, delta_days)

if __name__ == '__main__':
	main_2()
		
