import tuotrading as tt 
from datetime import date
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def bb3_scanner(BB3_list, start_date, end_date=date.today(), base_dir='data/data_2018'):
	result = {}

	for spread_name in BB3_list:
		data = tt.calculate_PnL(spread_name)

		# Calculate daily PnL
		daily_PnL = data.groupby(data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
		daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)

		# Calculate Sharpe Ratio between start and end date:
		temp = daily_PnL.loc[start_date:end_date]['PnL'].copy()
		sharpeRatio = temp.mean() / temp.std() * np.sqrt(len(temp))


		result[spread_name] = sharpeRatio

		print spread_name, sharpeRatio

	return result

def main():
	start_date = date(2018,5,1)
	print bb3_scanner(['GBL-ZN','GBL-ZN+.3*E6','R-ZN+.3*B6','ZN-J6'], start_date)

if __name__ == '__main__':
	main()
		
