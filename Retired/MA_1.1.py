import tuotrading as tt 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 

class Spread():
	def __init__(self, name):
		self.name = name
		self.data = tt.get_spread(name)['Spread'].to_frame('Spread')
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
	def plot_PnL(self):
		data['cumPnL'].plot()
		plt.show()




def main():
	print 'start...'
	spread = Spread('E6-C6')
	pnl = pd.DataFrame(index=spread.data.index)
	entry = 1.5
	exits = np.linspace(.5,.5,1)
	for exit in exits:
		print exit
		strt = MA_Strategy(spread, entry, exit, 35)
		name = str(exit)
		pnl[name] = strt.data['cumPnL']
	pnl.plot()
	plt.show()
	
if __name__ == '__main__':
	main()
