import argparse
import Dyn_EE
from datetime import date, timedelta

parser = argparse.ArgumentParser()
parser.add_argument('spread_name')
parser.add_argument('threshold', type=int)
args = parser.parse_args()

def test_run():
	spread_name = args.spread_name
	threshold = args.threshold

	end_date = date.today()
	start_date = end_date - timedelta(days=60)
	test_obj = Dyn_EE.Dyn_EE(spread_name, 'data/data_2018', 2.0, 0.5, threshold)
	test_obj.print_SharpeRatio(start_date, end_date)
	test_obj.plot_trade(start_date, end_date)



if __name__ == '__main__':
	test_run()