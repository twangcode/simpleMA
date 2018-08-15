import tuotrading as tt 
from datetime import date
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

def bb3_scanner(filename='data/BB3_list.csv', start_date=date(2018,1,1), end_date=date.today(), base_dir='data/data_2018'):
	result = {}
	BB3_list = pd.read_csv(filename, index_col='BB3_name')

	for row in BB3_list.itertuples():
		BB3_name = row[0]
		Threshold = row[1]
		data = tt.calculate_PnL(BB3_name, threshold=Threshold)

		# Calculate daily PnL
		daily_PnL = data.groupby(data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
		daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)

		# Calculate Sharpe Ratio between start and end date:
		temp = daily_PnL.loc[start_date:end_date]['PnL'].copy()
		sharpeRatio = temp.mean() / temp.std() * np.sqrt(len(temp))


		result[BB3_name] = sharpeRatio

		print BB3_name, sharpeRatio

	df_Sharpe = pd.DataFrame.from_dict({'Sharpe':result}).sort_values(by='Sharpe', ascending=False)

	return df_Sharpe

def main():
	# df = pd.read_csv('data/BB3_list.csv', index_col='BB3_name')
	# for row in df.itertuples():
	# 	print row[0]



	start_date = date(2018,7,1)
	print bb3_scanner(start_date=start_date)

if __name__ == '__main__':
	main()
		
