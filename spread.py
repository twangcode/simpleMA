import tuotrading as tt 
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

class Spread():
	def __init__(self, name, base_dir='data/data_2018'):
		self.name = name
		self.data = tt.get_spread(self.name, base_dir)['Spread'].to_frame('Spread')

	def calculate_MA(self, hour=48, bar_size=60, entry=2.0, exit=0.5):
		self.data['MA'] = self.data['Spread'].rolling(window=hour*bar_size).mean()
		self.data['STD'] = self.data['Spread'].rolling(window=hour*bar_size).std()
		self.data['UpperBand'] = self.data['MA'] + self.data['STD'] * entry
		self.data['LowerBand'] = self.data['MA'] - self.data['STD'] * entry
		self.data['LongExit'] = self.data['LowerBand'] + self.data['STD'] * entry * exit
		self.data['ShortExit'] = self.data['UpperBand'] - self.data['STD'] * entry * exit

	def between(self, start_dt=datetime.now().date().replace(month=1, day=1),\
				end_dt=datetime.today()):
		return self.data.loc[start_dt, end_dt]

	def print_components(self):
		print tt.read_spread_name(self.name)
	def print_spread_name(self):
		print self.name
	def get_spread_name(self):
		return self.name
	def print_spread_data(self):
		print self.data
	def get_spread_data(self):
		return self.data
	def plot(self):
		self.data.plot(title=self.name)
		plt.show()

def main():
	print 'START>>>>'
	print 
	test_sp = Spread('GBL-ZN')
	test_sp.calculate_MA()
	# test_sp.print_components()
	test_sp.print_spread_data()

if __name__ == '__main__':
	main()