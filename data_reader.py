import pandas as pd
import query_data as qd
import datetime
import os

###### A wrapper for get_norm_price:
#######################################
def data_reader(symbol, start_date, end_date, start_time=datetime.time(0,0,0), end_time=datetime.time(23,59,59), bar_size=60):
	######### Call get_norm_price
	raw_data = qd.get_norm_price(symbol, 'm', start_date, end_date, start_time, end_time, bar_size)
	######### Convert bar data from dict to dataFrame
	data = pd.DataFrame.from_dict({symbol:raw_data})
	return data

def main():
	start_date = datetime.date(2018,1,1)
	end_date = datetime.date.today()
	symbol_list = ['ZN', 'ZB', 'GBL', 'R', 'CGB', 'TS', 'A6', 'B6', 'C6', 'E6', 'GBS', 'GBM', 'GBX', 'ZF', 'ZT', 'GC', 'J6']

	os.system('clear')
	for symbol in symbol_list:
		data = data_reader(symbol, start_date, end_date)
		data.to_csv('{}.csv'.format(symbol))
		print("Saved data to {}.csv".format(symbol))
if __name__ == "__main__":
	main()
