from datetime import datetime
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


# read data from "/data". 
#	clean_data: boolean. Whether or not to exclude market opening and closing data points
# 				
def read_csv(symbol, clean_data=True):
	data = pd.read_csv('data/data_2018/{}.csv'.format(symbol), index_col=0, parse_dates=True)
	if clean_data:
		data = set_session_time(symbol, data)
	return data

#	Unfinished set_session function:
# 	Deleting unreliable data at the time of market opening and closing
#	Unfinished part: 1. Other exchanges besides US
#					2. Holiday
def set_session_time(symbol, data):
	if symbol in US_SESSION:
		data = data.between_time('17:02', '15:58')
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

def generate_position(data, entry=2.0, exit=0.5, threshold=20):
	data = calculate_MA(data, entry=entry, exit=exit)
	data['Position'] = None
	data['Position'] = np.where(data['Spread'] > (data['UpperBand'] + threshold), -1, None)
	data['Position'] = np.where(data['Spread'] < (data['LowerBand'] - threshold), 1, data['Position'])
	data['Position'] = np.where((data['Spread'] > (data['LongExit'] + threshold)) & (data['Spread'] < (data['ShortExit'] - threshold)), 0, data['Position'])
	data['Position'] = data['Position'].fillna(method='ffill')
	data['Position'] = data['Position'].fillna(0)
	return data

def Back_Test(data):
	# Calculate Cumulative PnL:
	data['Trade'] = data['Position'] - data['Position'].shift(1)
	data['Trade'] = np.where(data['Trade'].isnull(), data['Position'], data['Trade'])
	data['Price'] = data['Trade'] * data['Spread']
	data['MarketValue'] = data['Spread'] * data['Position']
	data['cumPnL'] = data['MarketValue'] - data['Price'].cumsum()
	data['plot_trade'] = data['Trade'] * data['Price']
	data['plot_trade'] = np.where(data['plot_trade'], data['plot_trade'], np.nan)

	data[['Spread', 'UpperBand', 'LowerBand', 'LongExit', 'ShortExit']].plot()
	data['plot_trade'].plot(style='g^')

	# Calculate daily_PnL:
	daily_PnL = data.groupby(data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
	daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)

	# Calculate incremental Sharpe Ratio

	daily_PnL['days'] = pd.Series(range(len(daily_PnL)), index = daily_PnL.index)
	daily_PnL['incr_mean'] = daily_PnL['PnL'].expanding(2).mean()
	daily_PnL['incr_std'] = daily_PnL['PnL'].expanding(2).std()
	daily_PnL['daily_SR'] = daily_PnL['incr_mean'] / daily_PnL['incr_std'] * np.sqrt(daily_PnL['days']) 

	return daily_PnL[['Position', 'cumPnL', 'PnL', 'daily_SR']]


def test_run():
	spread_name = 'GBL-ZN+.5*E6'
	threshold = 35

	data = get_spread(spread_name)
	data = generate_position(data, 2, .5)
	result = Back_Test(data)
	PnL = pd.DataFrame(index=result.index.copy())
	entrys = np.linspace(0.5, 4, 8)
	exits = np.linspace(.5, .5, 1)

	# data = generate_position(data, 1, .5)
	# Back_Test(data).plot()

	for entry in entrys:
		for exit in exits:

			data = generate_position(data, entry, exit)
			result = Back_Test(data)
			name = str(entry)+','+str(exit)
			temp = result.rename(columns={'cumPnL':name})
			print name
			print 
			print result['Position'].value_counts()
			PnL[name] = temp[name]
			# temp[name].plot(legend=True)
			# ax.legend(str(entry)+','+str(exit))
	# PnL['SUM'] = PnL.sum(axis=1)
	PnL.plot()

	plt.show()

if __name__ == '__main__':
	test_run()




