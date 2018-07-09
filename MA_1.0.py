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
	return data

def Trading_Signal_Long(data, entry=2.0, exit=0.5):
	# Check when price is above or below our entry or exit level
	# *** Important! This is not the final trading signal. This only tells us when price is below or above our entry or exit level. 
	data['Init_Long'] = np.where(data['Spread'] < (data['MA'] - data['STD'] * entry), 1, 0)
	data['Takeoff_Long'] = np.where(data['Spread'] > (data['MA'] - data['STD'] * entry * exit), -1, 0)
	
	
	result = data[(data['Init_Long'] + data['Takeoff_Long']) != 0].copy()
	trade = result[((result['Init_Long'] - result['Init_Long'].shift(1)) == 1) \
				 | ((result['Takeoff_Long'] - result['Takeoff_Long'].shift(1)) == -1)].copy()
	data=data.join(trade[['Init_Long', 'Takeoff_Long']], how='left', lsuffix='_1')
	data['Trade'] = data['Init_Long'] + data['Takeoff_Long']
	return data

def Trading_Signal_Short(data, entry=2.0, exit=0.5):
	data['Init_Short'] = np.where(data['Spread'] > (data['MA'] + data['STD'] * entry), -1, 0)
	data['Takeoff_Short'] = np.where(data['Spread'] < (data['MA'] + data['STD'] * entry * exit), 1, 0)

	result = data[(data['Init_Short'] + data['Takeoff_Short']) != 0].copy()
	trade = result[((result['Init_Short'] - result['Init_Short'].shift(1)) == -1) \
				 | ((result['Takeoff_Short'] - result['Takeoff_Short'].shift(1)) == 1)].copy()
	data=data.join(trade[['Init_Short', 'Takeoff_Short']], how='left', lsuffix='_1')
	data['Trade'] = data['Init_Short'] + data['Takeoff_Short']

	return data

def Trading_Signal(data, entry=2.0, exit=0.5):
	if {'Spread', 'MA', 'STD'}.issubset(data.columns):
		Trade = data[['Spread', 'MA', 'STD']].copy()
		Trade['Trigger_Long'] = np.where(Trade['Spread'] < (Trade['MA'] - Trade['STD'] * entry), 1, 0)
		Trade['Trigger_Takeoff_Long'] = np.where(Trade['Spread'] > (Trade['MA'] - Trade['STD'] * entry * exit), 1, 0)
		Trade['Trigger_Short'] = np.where(Trade['Spread'] > (Trade['MA'] + Trade['STD'] * entry), 1, 0)
		Trade['Trigger_Takeoff_Short'] = np.where(Trade['Spread'] < (Trade['MA'] + Trade['STD'] * entry * exit), 1, 0)

		Trade['Position'] = 0
		flag = 0
		for i in Trade.index:
			if Trade.at[i, 'Trigger_Long'] == 1:
				flag = 1
				Trade.at[i, 'Position'] = 1
			elif Trade.at[i, 'Trigger_Short'] == 1:
				flag = -1
				Trade.at[i, 'Position'] = -1
			elif (Trade.at[i, 'Trigger_Takeoff_Long'] + Trade.at[i, 'Trigger_Takeoff_Short']) == 1:
				Trade.at[i, 'Position'] = flag
			elif (Trade.at[i, 'Trigger_Takeoff_Long'] + Trade.at[i, 'Trigger_Takeoff_Short']) == 2:
				Trade.at[i, 'Position'] = 0
				flag = 0
		return Trade



def Back_Test(data):
	result = data[['Spread','Position']].copy()
	result['Trade'] = result['Position'] - result['Position'].shift(1)
	# result['Position'] = result['Trade'].cumsum()
	result['Price'] = result['Trade'] * result['Spread']
	result['CumPrice'] = result['Price'].cumsum()
	result['Value'] = result['Spread'] * result['Position']
	result['PnL'] = result['Value'] - result['CumPrice']
	return result


def test_run():
	data = get_spread('R-ZN+.3*B6')
	data = calculate_MA(data)
	# trade = Trading_Signal_Long(data)
	# trade = Trading_Signal_Short(data)

	trade = Trading_Signal(data)
	trade.to_csv('test.csv')

	result = Back_Test(trade)
	result.to_csv('test.csv')
	result['PnL'].plot()
	plt.show()

if __name__ == '__main__':
	test_run()
