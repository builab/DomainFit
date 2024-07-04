output_dir = 'solutions_tipcp_spike1'
log_file = 'solutions_tipcp_spike1/fit_logs.txt'

import pandas as pd
df = pd.read_csv(log_file, sep='\s*,\s*')
df.info()
df.dropna()
print(df)
#for col in df.columns:
	#print(col)
df.sort_values(['BH_adjusted_Pvalue', 'Corr_about_mean'], ascending=[True, False], inplace=True)
# df.sort_values(by = "Diff", inplace=True, ascending=False)

#print(df)
df.to_csv(output_dir + '/fit_logs_revised.csv', index=False)
