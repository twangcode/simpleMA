import tuotrading as tt 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from datetime import datetime, date, timedelta

class Dyn_EE():
	def __init__(self, spread_name, base_dir, entry, exit, threshold):
		self.data = tt.calculate_PnL(spread_name, base_dir, entry, exit, threshold)
		self.name = spread_name
	def print_name(self):
		print self.name
	def get_name(self):
		return self.name
	def print_data(self):
		print self.data
	def get_data(self):
		return self.data
	def to_csv(self, filename):
		self.data.to_csv(filename)
	
	# Unifinished plot trade function	
	def print_trade(self):
		trades = self.data[self.data['Trade'] != 0][['buy', 'sell']].copy()
		print trades
	def get_daily_PnL(self):
		# Calculate daily PnL
		daily_PnL = self.data.groupby(self.data.index.date).last()[['Position', 'cumPnL']].fillna(method='ffill').fillna(0)
		daily_PnL['PnL'] = daily_PnL['cumPnL'] - daily_PnL['cumPnL'].shift(1)
		return daily_PnL
	def get_SharpeRatio(self, start_date, end_date):
		# Calculate Sharpe Ratio between start and end date:
		daily_PnL = self.get_daily_PnL()
		pnl = daily_PnL.loc[start_date:end_date]['PnL'].copy()
		sharpeRatio = pnl.mean() / pnl.std() * np.sqrt(len(pnl))
		return sharpeRatio
	def print_SharpeRatio(self, start_date, end_date):
		print self.get_SharpeRatio(start_date, end_date)
	def plot_trade(self, start_date, end_date):
		plot_data = self.data.copy()
		# print plot_data
		plot_data = plot_data.loc[start_date:end_date]
		# temp = daily_PnL.loc[start_date:end_date]['PnL'].copy()
		plot_data[['Spread', 'MA', 'UpperBand', 'LowerBand', 'LongExit', 'ShortExit']].plot()
		plot_data['buy'].plot(style='g^')
		plot_data['sell'].plot(style='rv')
		plt.show()
	def plot_cumPnL(self):
		data['cumPnL'].plot()
		plt.show()

<<<<<<< HEAD
def test_run():
	spread_name = 'R+X'
	threshold = 35

	end_date = date.today()
	start_date = end_date - timedelta(days=60)
	test_obj = Dyn_EE(spread_name, 'data/data_2018', 2.0, 0.5, threshold)
	test_obj.plot_trade(start_date, end_date)
	test_obj.print_SharpeRatio(start_date, end_date)


if __name__ == '__main__':
	test_run()

=======
>>>>>>> 9d9e173a5fca2731c8bcbaf5e8987f161aa76e88
