import pandas as pd
import query_data as qd
import globalcontrol as gc 
import datetime
import os

# CBOT_PRODUCT = ['ZT', 'ZF', 'ZN', 'TN', 'ZB', 'UB']
# CME_PRODUCT = ['ES', 'NQ', 'YM', 'NKD', \
# 		'A6', 'B6', 'C6', 'E6', 'J6', 'M6', 'N6', 'S6', \
# 		'GC', 'HG', 'PA', 'PL', 'SI', \
# 		'CL', 'HO', 'NG', 'RB', 'ZC', 'ZL', 'ZM', 'ZS', 'ZW']
# EUREX_PRODUCT = ['AEX', 'DF', 'ESX', 'MX', 'BTP', 'GBL', 'GBM', 'GBX', 'GBS']
# ICE_PRODUCT = ['ICEDX'] ##, 'ICETF', 'LET', 'LGO', 'OIL', 'ICECC', 'ICECT', 'ICEKC', 'ICESB']
# LIFFE_PRODUCT = ['X', 'G', 'R']
# ASX_PRODUCT = ['TS', 'YS', 'YAP']
# TMX_PRODUCT = ['CGB', 'SXF']
# TYO_PRODUCT = ['BT']
# CME_GE_PRODUCT = ['GE4', 'GE5', 'GE6', 'GE7', 'GE8', 'GE9', 'GE10', 'GE11', 'GE12', 'GE13', 'GE14', \
# 		  'GE15', 'GE16', 'GE17', 'GE18', 'GE19', 'GE20', 'GE21', 'GE22', 'GE23', 'GE24']
# EUREX_U_PRODUCT = ['U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'U10', 'U11', 'U12']
# LIFFE_R_PRODUCT = ['L9', 'L10', 'L11', 'L12']


###### A wrapper for get_norm_price:
#######################################
def data_reader(symbol, start_date, end_date, start_time=datetime.time(0,0,0), end_time=datetime.time(23,59,59), bar_size=60):
	######### Call get_norm_price
	raw_data = qd.get_norm_price(symbol, 'm', start_date, end_date, start_time, end_time, bar_size)
	######### Convert bar data from dict to dataFrame
	data = pd.DataFrame.from_dict({symbol:raw_data})
	return data

def read_product(product_list, start_date, end_date, to_csv=True):
	for symbol in product_list:
		data = data_reader(symbol, start_date, end_date)
		print data.tail(1)
		if to_csv:
			data.to_csv('data/{}.csv'.format(symbol))
			print 'Save to {}.csv'.format(symbol) 

def get_product_list():
	GC = gc.GlobalControl()
	prod_list = GC.get_all_tags()
	return prod_list

def main():
	start_date = datetime.date(2018,1,1)
	end_date = datetime.date.today() - datetime.timedelta(days=2)
	
	os.system('clear')
	prod_list = get_product_list()

	read_product(prod_list, start_date, end_date)
	

if __name__ == "__main__":
	main()
