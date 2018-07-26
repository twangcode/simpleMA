import tuotrading as tt 
from spread import * 
from dynamic_EE import *
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

base_dir = 'data/data_2018'
spread_name = 'ZN+YM'
entries = np.linspace(.5, 4, 1)
exits = np.linspace(.1, 1, 1)
threshold = 35



def main():
	print 'start...'
	spread = Spread(spread_name, base_dir)
	pnl = pd.DataFrame(index=spread.data.index)
	for entry in entries:
		for exit in exits:
			strt = MA_Strategy(spread, entry, exit, threshold)
			name = 'Entry='+str(entry)+','+'Exit='+str(exit)
			pnl[name] = strt.data['cumPnL']
	pnl.plot()
	plt.show()
	
if __name__ == '__main__':
	main()