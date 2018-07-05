from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_csv(symbol):
	data = pd.read_csv('data/data_2017/{}.csv'.format(symbol), index_col=0, parse_dates=True)
	return data

def Break_Components(str):
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
	comp_dict = Break_Components(name)
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
	data['Upper_Band'] = data['MA'] + 2 * data['STD']
	data['Lower_Band'] = data['MA'] - 2 * data['STD']
	return data

def Trading_Signal(data):
	data['Regime'] = np.where(data['Spread'] > data['Upper_Band'], 1, 0)
	data['Regime'] = np.where(data['Spread'] < data['Lower_Band'], -1, data['Regime'])
	return data

def test_run():
	data = get_spread('TS-ZN+.3*A6')
	print data
	data = calculate_MA(data)
	data = Trading_Signal(data)
	data[['Spread','MA','Upper_Band','Lower_Band']].plot()
	print data['Regime'].value_counts()
	print (data['Regime'] - data['Regime'].shift(1)).value_counts()
	plt.show()

if __name__ == '__main__':
	test_run()
