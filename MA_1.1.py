import tuotrading as tt 

class Spread():
	def __init__(self, name):
		self.name = name
		self.data = tt.get_spread(name)['Spread']

	def print_name(self):
		print self.name

	def print_spread_data(self):
		print type(self.data)

class MA_Strategy():
	def __init__(self, spread, entry, exit, threshold):
		self.data = spread.data.to_frame('Spread')
		self.data = tt.generate_position(self.data, entry, exit, threshold)
		self.data = tt.calculate_PnL(self.data, plot_trade=False, plot_cumPnL=False)
		self.name = spread.name
	def print_name(self):
		print self.name
	def print_data(self):
		print self.data
	def plot(self, content='all'):
		content = content.lower()
		if content is 'trade':
			tt.calculate_PnL(self.data, plot_trade=True, plot_cumPnL=False)
		elif content is 'cumPnL':
			tt.calculate_PnL(self.data, plot_trade=False, plot_cumPnL=True)
		elif content is 'all':
			tt.calculate_PnL(self.data, plot_trade=True, plot_cumPnL=True)
		else:
			print('Wrong Input')
			tt.calculate_PnL(self.data, plot_trade=False, plot_cumPnL=False)




def main():
	spread = Spread('GBL-ZN+.5*E6')
	strt = MA_Strategy(spread, 2, 0.5, 35)
	strt.print_data()
	
if __name__ == '__main__':
	main()
