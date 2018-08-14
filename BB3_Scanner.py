import tuotrading as tt 

def bb3_scanner(BB3_list, start_dt, end_dt, base_dir='data/data_2018'):
	result = {}

	for spread_name in BB3_list:
		data = tt.get_spread(spread_name, base_dir)
		
