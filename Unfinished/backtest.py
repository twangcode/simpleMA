import tuotrading as tt 
from spread import * 
from dynamic_EE import *
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

base_dir = 'data/data_2018'
spread_name = 'ZN+YM'
entries = np.linspace(.5, 4, 1)
exits = np.linspace(.1, 1, 1)
threshold = 35

def find_opt_entry_exit(spread_name, base_dir, entries, exits, threshold):
	spread = Spread(spread_name, base_dir)
	pnl = pd.DataFrame(index=spread.data.index)
	for entry in entries:
		for exit in exits:
			strt = MA_Strategy(spread, entry, exit, threshold)
			name = 'Entry='+str(entry)+','+'Exit='+str(exit)
			pnl[name] = strt.data['cumPnL']
	pnl.plot()
	plt.show() 

def main():
	print 'start...'
	find_opt_entry_exit(spread_name, base_dir, entries, exits, threshold)
	
if __name__ == '__main__':
	main()