import tuotrading as tt 

class Spread():
	def __init__(self, name):
		self.name = name
		self.data = tt.get_spread(name)

	def print_name(self):
		print self.name

	def print_spread_data(self):
		print self.data

	def plot_cumPnL(self):
		self.data


def main():
	spread = Spread('GBL-ZN+.5*E6')
	spread.print_spread_data()

if __name__ == '__main__':
	main()
