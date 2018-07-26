import tuotrading as tt 
from spread import * 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

class MA_Strategy():
	def __init__(self, spread, entry, exit, threshold):
		# self.data = spread.get_spread_data().to_frame('Spread')
		# self.data = tt.generate_position(self.data, entry, exit, threshold)
		self.data = tt.calculate_PnL(spread, entry, exit, threshold)
		self.name = spread.name
	def print_name(self):
		print self.name
	def get_name(self):
		return self.name
	def print_data(self):
		print self.data
	def get_data(self):
		return self.data
	def plot_trade(self):
		self.data[['Spread', 'MA', 'UpperBand', 'LowerBand', 'LongExit', 'ShortExit']].plot()
		self.data['buy'].plot(style='g^')
		self.data['sell'].plot(style='rv')
		plt.show()
	def plot_cumPnL(self):
		data['cumPnL'].plot()
		plt.show()

