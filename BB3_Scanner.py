import os
import tuotrading as tt 
from datetime import date, timedelta
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def bb3_backtest(spread_name, threshold, base_dir, start_date, end_date, entry, exit):
	data = tt.calculate_PnL(spread_name, base_dir, entry, exit, threshold)

	# Calculate daily PnL
	daily_PnL = data.groupby(data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
	daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)

	# Calculate Sharpe Ratio between start and end date:
	temp = daily_PnL.loc[start_date:end_date]['PnL'].copy()
	sharpeRatio = temp.mean() / temp.std() * np.sqrt(len(temp))

	# Calculate drawdown
	daily_PnL['MaxProfit'] = daily_PnL['cumPnL'].cummax()
	

	return sharpeRatio

def bb3_backtest_delta_days(spread_name, threshold, base_dir, end_date, delta_days, entry, exit):
	start_date = end_date - timedelta(days=delta_days)
	sharpeRatio = bb3_backtest(spread_name, threshold, base_dir, start_date, end_date, entry, exit)
	return sharpeRatio


def bb3_scanner(BB3_list_filename, base_dir, start_date, end_date, entry=2.0, exit=0.5):
	result = {}
	BB3_list = pd.read_csv(BB3_list_filename, index_col='BB3_name')

	for row in BB3_list.itertuples():
		spread_name = row[0]
		threshold = row[1]
		
		sharpeRatio = bb3_backtest(spread_name, threshold, base_dir, start_date, end_date, entry, exit)

		result[spread_name] = sharpeRatio

		# print spread_name, sharpeRatio

	df_Sharpe = pd.DataFrame.from_dict({'Sharpe':result}).sort_values(by='Sharpe', ascending=False)

	return df_Sharpe

def bb3_scanner_delta_days(BB3_list_filename, base_dir, end_date, delta_days, entry=2.0, exit=0.5):
	start_date = end_date - timedelta(days=delta_days)
	df_Sharpe = bb3_scanner(BB3_list_filename, base_dir, start_date, end_date, entry, exit)
	return df_Sharpe

def main():
	end_date = date.today()
	start_date = end_date - timedelta(days=30)
	start_date_2 = end_date - timedelta(days=10)

	base_dir = 'data/data_2018'
	bb3_list_folder = 'data/BB3'
	bb3_file_list = os.listdir(bb3_list_folder)
	for file in bb3_file_list:
		if file.endswith('.csv'):
			SR_30d = bb3_scanner(os.path.join(bb3_list_folder,file), base_dir, start_date, end_date)
			SR_30d = SR_30d.rename(columns={'Sharpe':'Sharpe_30'})
			SR_10d = bb3_scanner(os.path.join(bb3_list_folder,file), base_dir, start_date_2, end_date)
			SR_10d = SR_10d.rename(columns={'Sharpe':'Sharpe_10'})
			SR = SR_10d.join(SR_30d)
			SR = SR.sort_values(by='Sharpe_10', ascending=False)
			SR.to_csv('data/{}.csv'.format(file[:-4]+'_log'))
			print 'finished '+'data/{}.csv'.format(file[:-4]+'_log')
	

def main_2():
	spread_name = 'CGB+C6'
	threshold = 15
	entry = 2.0
	exit = 0.5
	start_date = date(2018,7,1)
	end_date = date.today()
	delta_days = 60
	base_dir = 'data/data_2018'
	print bb3_backtest(spread_name, threshold, base_dir, start_date, end_date, entry, exit)
	print bb3_backtest_delta_days(spread_name, threshold, base_dir, end_date, delta_days, entry, exit)

if __name__ == '__main__':
	main()
		
