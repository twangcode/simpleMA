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
ICE_PRODUCT = ['ICEDX'] ##, 'ICETF', 'LET', 'LGO', 'OIL', 'ICECC', 'ICECT', 'ICEKC', 'ICESB']
LIFFE_PRODUCT = ['X', 'G', 'R']
ASX_PRODUCT = ['TS', 'YS', 'YAP']
TMX_PRODUCT = ['CGB', 'SXF']
TYO_PRODUCT = ['BT']
CME_GE_PRODUCT = ['GE9', 'GE11']
EUREX_U_PRODUCT = ['U7', 'U11']
LIFFE_R_PRODUCT = ['L12']


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
		print data.tail(1)
		if to_csv:
			data.to_csv('{}.csv'.format(symbol))
			print 'Save to {}.csv'.format(symbol) 

def main():
	start_date = datetime.date(2018,1,1)
	end_date = datetime.date.today() - datetime.timedelta(days=2)
	
	os.system('clear')
	
	# read_exchange(CBOT_PRODUCT, start_date, end_date)
	# print 'Finished CBOT'
	# print

	# read_exchange(CME_PRODUCT, start_date, end_date)
	# print 'Finished CME'
	# print
	
	# read_exchange(EUREX_PRODUCT, start_date, end_date)
	# print 'Finished EUREX'
	# print
	

	# read_exchange(ICE_PRODUCT, start_date, end_date)
	# print 'Finished ICE'
	# print
	
	# read_exchange(LIFFE_PRODUCT, start_date, end_date)
	# print 'Finished LIFFE'
	# print
	
	# read_exchange(ASX_PRODUCT, start_date, end_date)
	# print 'Finished ASX'
	# print
	
	# read_exchange(TMX_PRODUCT, start_date, end_date)
	# print 'Finished MOTREAL'
	# print
	
	# read_exchange(TYO_PRODUCT, start_date, end_date)
	# print 'Finished TYOKO'
	# print

	read_exchange(CME_GE_PRODUCT, start_date, end_date)
	print 'Finished CME_GE'
	print 

	read_exchange(EUREX_U_PRODUCT, start_date, end_date)
	print 'Finished EUREX_U'
	print 

	read_exchange(LIFFE_R_PRODUCT, start_date, end_date)
	print 'Finished LIFFE_R'
	print 
	

if __name__ == "__main__":
	main()
