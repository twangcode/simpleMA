from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def test_run():
	data = read_csv('A6')
	data_MA = calculate_MA(data)
	plot_result(data_MA)

def read_csv(symbol):
	data = pd.read_csv('data/data_2017/{}.csv'.format(symbol), index_col=0)
	return data

def calculate_MA(data):
	data['MA'] = data.rolling(window=48*60).mean()
	data['STD'] = data['A6'].rolling(window=48*60).std() * np.sqrt(48*60)
	data['Upper_Band'] = data['MA']+2*data['STD']
	data['Lower_Band'] = data['MA']-2*data['STD']
	data_ma = data[['A6','MA','Upper_Band','Lower_Band']]	
	return data_ma

def print_result(data):
	print data

def plot_result(data):
	data.dropna()
	data.plot.line()
	plt.show()
    
if __name__ == '__main__':
	test_run()
