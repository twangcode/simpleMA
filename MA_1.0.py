from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_csv(symbol):
	data = pd.read_csv('data/data_2018/{}.csv'.format(symbol), index_col=0, parse_dates=True)
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

def calculate_MA(data, hour=48, bar_size=60, entry=2.0, exit=0.5):
	data['MA'] = data['Spread'].rolling(window=hour*bar_size).mean()
	data['STD'] = data['Spread'].rolling(window=hour*bar_size).std()
	data['UpperBand'] = data['MA'] + data['STD'] * entry
	data['LowerBand'] = data['MA'] - data['STD'] * entry
	data['LongExit'] = data['LowerBand'] + data['STD'] * entry * exit
	data['ShortExit'] = data['UpperBand'] - data['STD'] * entry * exit
	return data


def generate_position(data):
	data['Position'] = None
	data['Position'] = np.where(data['Spread'] > data['UpperBand'], -1, None)
	data['Position'] = np.where(data['Spread'] < data['LowerBand'], 1, data['Position'])
	data['Position'] = np.where((data['Spread'] > data['LongExit']) & (data['Spread'] < data['ShortExit']), 0, data['Position'])
	data['Position'] = data['Position'].fillna(method='ffill')
	return data



# def Trading_Signal(data, entry=2.0, exit=0.5):
# 	if {'Spread', 'MA', 'STD'}.issubset(data.columns):
# 		Trade = data[['Spread', 'MA', 'STD']].copy()
# 		Trade['Trigger_Long'] = np.where(Trade['Spread'] < (Trade['MA'] - Trade['STD'] * entry), 1, 0)
# 		Trade['Trigger_Takeoff_Long'] = np.where(Trade['Spread'] > (Trade['MA'] - Trade['STD'] * entry * exit), 1, 0)
# 		Trade['Trigger_Short'] = np.where(Trade['Spread'] > (Trade['MA'] + Trade['STD'] * entry), 1, 0)
# 		Trade['Trigger_Takeoff_Short'] = np.where(Trade['Spread'] < (Trade['MA'] + Trade['STD'] * entry * exit), 1, 0)

# 		Trade['Position'] = 0
# 		flag = 0
# 		for i in Trade.index:
# 			if Trade.at[i, 'Trigger_Long'] == 1:
# 				flag = 1
# 				Trade.at[i, 'Position'] = 1
# 			elif Trade.at[i, 'Trigger_Short'] == 1:
# 				flag = -1
# 				Trade.at[i, 'Position'] = -1
# 			elif (Trade.at[i, 'Trigger_Takeoff_Long'] + Trade.at[i, 'Trigger_Takeoff_Short']) == 1:
# 				Trade.at[i, 'Position'] = flag
# 			elif (Trade.at[i, 'Trigger_Takeoff_Long'] + Trade.at[i, 'Trigger_Takeoff_Short']) == 2:
# 				Trade.at[i, 'Position'] = 0
# 				flag = 0
# 		return Trade



def Back_Test(data):
	# Calculate PnL:
	result = data[['Spread','Position']].copy()
	result['Trade'] = result['Position'] - result['Position'].shift(1)
	result['Price'] = result['Trade'] * result['Spread']
	result['CumPrice'] = result['Price'].cumsum()
	result['Value'] = result['Spread'] * result['Position']
	result['PnL'] = result['Value'] - result['CumPrice']
	# Calculate Sharpe_Ratio:
	

	return result


def test_run():
	data = get_spread('2*GBL-GBM-GBX')
	data = calculate_MA(data)

	data = generate_position(data)
	# trade = Trading_Signal(data)

	result = Back_Test(data)
	result['PnL'].plot()
	
	plt.show()

if __name__ == '__main__':
	test_run()
