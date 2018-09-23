import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta
from pandas.tseries.offsets import BDay 

# Set up session time:
US_SESSION = ['ZT', 'ZF', 'ZN', 'TN', 'ZB', 'UB' \
				'ES', 'NKD', 'YM', 'NQ'\
				'J6', 'A6', 'B6', 'C6', 'E6', 'M6', 'N6', \
				'PL', 'GC', 'SI', 'HG']
UK_SESSION = ['R']
EU_SESSION = ['GBS', 'GBM', 'GBL', 'GBX', 'ESX', 'DF']
AU_SESSION = ['TS', 'YS', 'YAP']
CA_SESSION = ['CGB']

def symbol_to_path(symbol, base_dir):
	return os.path.join(base_dir, '{}.csv'.format(str(symbol)))


# read data from "/data". 
#	clean_data: boolean. Whether or not to exclude market opening and closing data points
# 				
def read_csv(symbol, base_dir, clean_data=True):
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

def get_spread(name, base_dir):
	comp_dict = read_spread_name(name)
	data = read_csv(comp_dict.keys()[0], base_dir) * comp_dict[comp_dict.keys()[0]]
	
	for item in comp_dict.keys():
		if item != comp_dict.keys()[0]:
			data_temp = read_csv(item, base_dir) * comp_dict[item]
			data = data.join(data_temp, how='inner')

	data['Spread'] = data.sum(axis=1)
	return data[['Spread']]	

def generate_position(data, entry, exit, threshold):
	data = calculate_MA(data, entry, exit)
	data['Position'] = None
	data['Position'] = np.where(data['Spread'] > (data['UpperBand'] + threshold), -1, None)
	data['Position'] = np.where(data['Spread'] < (data['LowerBand'] - threshold), 1, data['Position'])
	data['Position'] = np.where((data['Spread'] > (data['LongExit'] + threshold)) & (data['Spread'] < (data['ShortExit'] - threshold)), 0, data['Position'])
	data['Position'] = data['Position'].fillna(method='ffill')
	data['Position'] = data['Position'].fillna(0)
	return data

def calculate_PnL(spread_name, base_dir, entry, exit, threshold):
	data = generate_position(spread_name, base_dir, entry, exit, threshold)
	# Calculate Cumulative PnL:
	data['Trade'] = data['Position'] - data['Position'].shift(1)
	data['Trade'] = np.where(data['Trade'].isnull(), data['Position'], data['Trade'])
	data['Price'] = data['Trade'] * data['Spread']
	data['MarketValue'] = data['Spread'] * data['Position']
	data['cumPnL'] = data['MarketValue'] - data['Price'].cumsum()
	data['buy'] = np.where(data['Trade'] > 0,  data['Price'] / data['Trade'], np.nan)
	data['sell'] = np.where(data['Trade'] < 0,  data['Price'] / data['Trade'], np.nan)
	return data

class Dyn_EE():
	def __init__(self, spread_name, start_dt, end_dt, entry=2, exit=.5, threshold=10):
		self.name = spread_name
		self.data = None
		self.start_date = pd.to_datetime(start_dt)
		self.end_date = pd.to_datetime(end_dt)
		self.entry = entry
		self.exit = exit
		self.threshold = threshold

	# Access data in Dyn_EE:
	def print_name(self):
		print self.name
	def get_name(self):
		return self.name
	def print_data(self):
		print self.data
	def get_data(self):
		return self.data

	# Output to CSV:
	def to_csv(self, filename):
		self.data.to_csv(filename)

	# Read-in Data:
	def read_data(self, base_dir):
		self.data = get_spread(self.name, base_dir)

	# Generate bolinger bands:
	def bbands(self, hour=48, bar_size=60):
		self.data['MA'] = self.data['Spread'].rolling(window=hour*bar_size).mean()
		self.data['STD'] = self.data['Spread'].rolling(window=hour*bar_size).std()
		self.data['UpperBand'] = self.data['MA'] + self.data['STD'] * self.entry
		self.data['LowerBand'] = self.data['MA'] - self.data['STD'] * self.entry
		self.data['LongExit'] = self.data['LowerBand'] + self.data['STD'] * self.entry * self.exit
		self.data['ShortExit'] = self.data['UpperBand'] - self.data['STD'] * self.entry * self.exit
	
		


def main():
	test = Dyn_EE('GBL-ZN', '20180901', datetime.now())
	test.read_data('data/data_2018')
	test.bbands()
	test.print_data()

if __name__ == '__main__':
	main()
