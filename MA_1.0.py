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
		[factor, prod] = item.split('*')
		comp_dict[prod] = float(factor)
	return comp_dict

def get_spread(name):
	TS = read_csv('TS')
	ZN = read_csv('ZN')
	A6 = read_csv('A6')
	data = TS.join(ZN, how='inner')
	data = data.join(A6, how='inner')
	data[name] = data['TS'] - data['ZN'] + .3 * data['A6']
	data[name].dropna()
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
	data = get_spread('Spread')
	data = calculate_MA(data)
	data = Trading_Signal(data)
	# data[['Spread','MA','Upper_Band','Lower_Band']].plot()
	print data['Regime'].value_counts()
	print (data['Regime'] - data['Regime'].shift(1)).value_counts()
	# plt.show()

if __name__ == '__main__':
	test_run()
