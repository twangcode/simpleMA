import tuotrading as tt 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

class Spread():
	def __init__(self, name, base_dir):
		self.name = name
		self.data = tt.get_spread(name, base_dir)['Spread'].to_frame('Spread')
	def print_spread_name(self):
		print self.name
	def get_spread_name(self):
		return self.name
	def print_spread_data(self):
		print type(self.data)
	def get_spread_data(self):
		return self.data
	def plot(self):
		self.data.plot(title=self.name)
		plt.show()