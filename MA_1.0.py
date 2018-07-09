from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_csv(symbol):
	data = pd.read_csv('data/data_2017/{}.csv'.format(symbol), index_col=0, parse_dates=True)
	return data

def read_spread_name(str):
	comp_dict = {}
	comp_list = str.replace('-', ' -').replace('+', ' +').split(' ')
	for item in comp_list:
		if '*' in item:
			[factor, prod] = item.split('*')
		elif item[0] == '-':
			[factor, prod] = [-1, item[1:]]
		else:
			[factor, prod] = [1, item]
		comp_dict[prod] = float(factor)
	return comp_dict

def get_spread(name):
	comp_dict = read_spread_name(name)
	data = read_csv(comp_dict.keys()[0]) * comp_dict[comp_dict.keys()[0]]
	
	for item in comp_dict.keys():
		if item != comp_dict.keys()[0]:
			data_temp = read_csv(item) * comp_dict[item]
			data = data.join(data_temp, how='inner')

	data['Spread'] = data.sum(axis=1)
	return data

def calculate_MA(data):
	data['MA'] = data['Spread'].rolling(window=48*60).mean()
	data['STD'] = data['Spread'].rolling(window=48*60).std()
	# data['Upper_Band'] = data['MA'] + 2 * data['STD']
	# data['Lower_Band'] = data['MA'] - 2 * data['STD']
	return data

def Trading_Signal(data, entry=2.0, exit=0.5):
	data['Init_Long'] = np.where(data['Spread'] < (data['MA'] - data['STD'] * entry), 1, 0)
	data['Takeoff_Long'] = np.where(data['Spread'] > (data['MA'] - data['STD'] * entry * exit), 1, 0)
	result = data[(data['Init_Long'] + data['Takeoff_Long']) != 0].copy()
	result['Init_Long_1'] = result['Init_Long'] - result['Init_Long'].shift(1)
	result['Takeoff_Long_1'] = result['Takeoff_Long'] - result['Takeoff_Long'].shift(1)
	# data['temp'] = data['Init_Long'] + data['Takeoff_Long']
	# data['Position'] = np.trunc((data['MA'] - data['Spread']) / data['STD'])
	# data['Position'] = np.where(data['Position'].isnull(), 0, data['Position'])
	# data['Trade'] = data['Position'] - data['Position'].shift(1)
	# data['Price'] = data['Trade'] * data['Spread']
	# data['CumPrice'] = data['Price'].cumsum()
	# data['Value'] = data['Spread'] * data['Position']
	# data['PnL'] = data['Value'] - data['CumPrice']
	# data['Position'] = np.where(data['Spread'] > data['Upper_Band'], 1, 0)
	# data['Position'] = np.where(data['Spread'] < data['Lower_Band'], -1, data['Position'])
	return result

def test_run():
	data = get_spread('R-ZN+.3*B6')
	data = calculate_MA(data)
	result = Trading_Signal(data)
	# data[['Spread', 'Upper_Band', 'Lower_Band']].plot()
	
	result[(result['Init_Long_1'] == 1) | (result['Takeoff_Long_1'] == 1)].to_csv('test.csv')
	# data[['Spread','MA']].plot()
	# data[['Spread', 'Position', 'Trade', 'Price', 'CumPrice', 'Value', 'PnL']].to_csv('test_1.csv')
	# data[data['Trade'] != 0].to_csv('test.csv')
	# data['PnL'].plot()
	# print (data['Position'] - data['Position'].shift(1)).value_counts()
	plt.show()

if __name__ == '__main__':
	test_run()
