import tuo_trading as tt 
import datetime
from dateutil import parser

def group_by_day(spread_name, start_date='2018-07-04', end_date=datetime.date.today()):
	# Get data:
	data = tt.get_spread_data(spread_name)

	# Slice data based on start_date and end_date, including up to 5 more previous days to calculate moving average:
	start_date = parser.parse(start_date) - datetime.timedelta(5)
	data = data.loc[start_date:end_date]

	# Get all trading days in data:
	dates = sorted(data.groupby(data.index.date).groups.keys())

	# Get daily data for each trading day as daily_data
	for date in dates:
		daily_data = data.groupby(data.index.date).get_group(date)
		daily_data = daily_data[1:-1]
		print len(daily_data)



def main():
	spread_name = 'GBL-ZN+.3*E6'
	group_by_day(spread_name)
	


if __name__ == '__main__':
	main()