import tuo_trading as tt 

def main():
	data = tt.get_spread_data('TS-ZN')
	print data

if __name__ == '__main__':
	main()