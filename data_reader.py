import pandas as pd
import query_data as qd
import datetime
import os

CBOT_PRODUCT = ['ZT', 'ZF', 'ZN', 'TN', 'ZB', 'UB']
CME_PRODUCT = ['ES', 'NQ', 'YM', 'NKD', \
		'A6', 'B6', 'C6', 'E6', 'J6', 'M6', 'N6', 'S6', \
		'GC', 'HG', 'PA', 'PL', 'SI', \
		'CL', 'HO', 'NG', 'RB', 'ZC', 'ZL', 'ZM', 'ZS', 'ZW']
EUREX_PRODUCT = ['AEX', 'DF', 'ESX', 'MX', 'BTP', 'GBL', 'GBM', 'GBX', 'GBS']
ICE_PRODUCT = ['ICETF', 'ICEDX', 'LET', 'LGO', 'OIL', 'ICECC', 'ICECT', 'ICEKC', 'ICESB']
LIFFE_PRODUCT = ['X', 'G', 'R']
SFE_PRODUCT = ['TS', 'YS', 'YAP']
MO_PRODUCT = ['CGB', 'SXF']
TYO_PRODUCT = ['BT']


###### A wrapper for get_norm_price:
#######################################
def data_reader(symbol, start_date, end_date, start_time=datetime.time(0,0,0), end_time=datetime.time(23,59,59), bar_size=60):
	######### Call get_norm_price
	raw_data = qd.get_norm_price(symbol, 'm', start_date, end_date, start_time, end_time, bar_size)
	######### Convert bar data from dict to dataFrame
	data = pd.DataFrame.from_dict({symbol:raw_data})
	return data

def read_exchange(exchange_name, start_date, end_date, to_csv=True):
	for symbol in exchange_name:
		data = data_reader(symbol, start_date, end_date)
		if to_csv:
			data.to_csv('{}.csv'.format(symbol))
			print 'Save to {}.csv'.format(symbol) 

def main():
	start_date = datetime.date(2018,1,1)
	end_date = datetime.date.today()
	
	os.system('clear')
	
	read_exchange(CBOT_PRODUCT, start_date, end_date)
	print 'Finished CBOT'
	print
	read_exchange(CME_PRODUCT, start_date, end_date)
	print 'Finished CME'
	print
	
	read_exchange(EUREX_PRODUCT, start_date, end_date)
	print 'Finished EUREX'
	print
	
	read_exchange(ICE_PRODUCT, start_date, end_date)
	print 'Finished ICE'
	print
	
	read_exchange(LIFFE_PRODUCT, start_date, end_date)
	print 'Finished LIFFE'
	print
	
	read_exchange(SFE_PRODUCT, start_date, end_date)
	print 'Finished SFE'
	print
	
	read_exchange(MO_PRODUCT, start_date, end_date)
	print 'Finished MOTREAL'
	print
	
	read_exchange(TYO_PRODUCT, start_date, end_date)
	print 'Finished TYOKO'
	print
	

if __name__ == "__main__":
	main()
