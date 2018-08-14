import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set up session time:
US_SESSION = ['ZT', 'ZF', 'ZN', 'TN', 'ZB', 'UB' \
				'ES', 'NKD', 'YM', 'NQ'\
				'J6', 'A6', 'B6', 'C6', 'E6', 'M6', 'N6', \
				'PL', 'GC', 'SI', 'HG']
UK_SESSION = ['R']
EU_SESSION = ['GBS', 'GBM', 'GBL', 'GBX', 'ESX', 'DF']
AU_SESSION = ['TS', 'YS', 'YAP']
CA_SESSION = ['CGB']

def symbol_to_path(symbol, base_dir='data'):
	return os.path.join(base_dir, '{}.csv'.format(str(symbol)))


# read data from "/data". 
#	clean_data: boolean. Whether or not to exclude market opening and closing data points
# 				
def read_csv(symbol, base_dir='data', clean_data=True):
	data = pd.read_csv(symbol_to_path(symbol, base_dir), index_col=0, parse_dates=True)
	if clean_data:
		data = set_session_time(symbol, data)
	return data

#	Unfinished set_session function:
# 	Deleting unreliable data at the time of market opening and closing
#	Unfinished part: 1. Other exchanges besides US
#					2. Holiday
def set_session_time(symbol, symbol_data):
	if symbol in US_SESSION:
		symbol_data = symbol_data.between_time('17:02', '15:58')
	elif symbol in UK_SESSION:
		symbol_data = symbol_data.between_time('2:02', '11:58')
	elif symbol in EU_SESSION:
		symbol_data = symbol_data.between_time('1:02', '14:58')
	elif symbol in AU_SESSION:
		symbol_data = symbol_data.between_time('17:32', '15:28')
	elif symbol in CA_SESSION:
		symbol_data = symbol_data.between_time('05:02', '15:28')
	return symbol_data

def read_spread_name(str):
	comp_dict = {}
	comp_list = str.replace('-', ' -').replace('+', ' +').split(' ')
	for item in comp_list:
		if '*' in item:
			[factor, prod] = item.split('*')
		elif item[0] == '-':
			[factor, prod] = [-1, item[1:]]
		elif item[0] == '+':
			[factor, prod] = [1, item[1:]]
		else:
			[factor, prod] = [1, item]
		comp_dict[prod] = float(factor)
	return comp_dict

def get_spread(name, base_dir='data/data_2018'):
	comp_dict = read_spread_name(name)
	data = read_csv(comp_dict.keys()[0], base_dir) * comp_dict[comp_dict.keys()[0]]
	
	for item in comp_dict.keys():
		if item != comp_dict.keys()[0]:
			data_temp = read_csv(item, base_dir) * comp_dict[item]
			data = data.join(data_temp, how='inner')

	data['Spread'] = data.sum(axis=1)
	return data

def calculate_MA(spread, hour=48, bar_size=60, entry=2.0, exit=0.5):
	data = get_spread(spread)
	data['MA'] = data['Spread'].rolling(window=hour*bar_size).mean()
	data['STD'] = data['Spread'].rolling(window=hour*bar_size).std()
	data['UpperBand'] = data['MA'] + data['STD'] * entry
	data['LowerBand'] = data['MA'] - data['STD'] * entry
	data['LongExit'] = data['LowerBand'] + data['STD'] * entry * exit
	data['ShortExit'] = data['UpperBand'] - data['STD'] * entry * exit
	return data

def generate_position(spread, entry=2.0, exit=0.5, threshold=20):
	data = calculate_MA(spread, entry=entry, exit=exit)
	data['Position'] = None
	data['Position'] = np.where(data['Spread'] > (data['UpperBand'] + threshold), -1, None)
	data['Position'] = np.where(data['Spread'] < (data['LowerBand'] - threshold), 1, data['Position'])
	data['Position'] = np.where((data['Spread'] > (data['LongExit'] + threshold)) & (data['Spread'] < (data['ShortExit'] - threshold)), 0, data['Position'])
	data['Position'] = data['Position'].fillna(method='ffill')
	data['Position'] = data['Position'].fillna(0)
	return data

def calculate_PnL(spread, entry=2.0, exit=0.5, threshold=20):
	data = generate_position(spread, entry, exit, threshold)
	# Calculate Cumulative PnL:
	data['Trade'] = data['Position'] - data['Position'].shift(1)
	data['Trade'] = np.where(data['Trade'].isnull(), data['Position'], data['Trade'])
	data['Price'] = data['Trade'] * data['Spread']
	data['MarketValue'] = data['Spread'] * data['Position']
	data['cumPnL'] = data['MarketValue'] - data['Price'].cumsum()
	data['buy'] = np.where(data['Trade'] > 0,  data['Price'] / data['Trade'], np.nan)
	data['sell'] = np.where(data['Trade'] < 0,  data['Price'] / data['Trade'], np.nan)
	return data