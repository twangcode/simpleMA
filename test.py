import pandas as pd
import matplotlib.pyplot as plt 
import tuotrading as tt 

df1 = tt.read_csv('A6', base_dir='data', clean_data=False)
df2 = tt.read_csv('A6', base_dir='data/data_2018', clean_data=False)
df2 = df2.rename(columns={'A6': 'A6_Old'})

df = df1.join(df2, how='outer')
df['diff'] = df['A6'] - df['A6_Old']
print df['diff'].sum()
