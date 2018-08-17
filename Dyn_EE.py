import tuotrading as tt 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from datetime import date, timedelta

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
	def plot_trade(self):
		self.data[['Spread', 'MA', 'UpperBand', 'LowerBand', 'LongExit', 'ShortExit']].plot()
		self.data['buy'].plot(style='g^')
		self.data['sell'].plot(style='rv')
		plt.show()
	def plot_cumPnL(self):
		data['cumPnL'].plot()
		plt.show()

def test_run():
	test_obj = Dyn_EE('GBL-ZN', 'data/data_2018', 2.0, 0.5, 30)
	test_obj.print_SharpeRatio(date(2018,8,1), date(2018,8,10))


if __name__ == '__main__':
	test_run()

