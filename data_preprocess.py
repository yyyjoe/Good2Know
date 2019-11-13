import csv
import re
import pandas as pd
import sys
if(len(sys.argv)<2):
	print("Please specify input file_name")
	sys.exit(2)


dir="data/"
file_name = sys.argv[1]
print("Process: ", file_name)
df = pd.read_csv(dir + "table-"+file_name+".csv")
drop_list=[]
for i, row in df.iterrows():
	df.at[i,"Text"] = re.sub(r'[^a-zA-Z]+', ' ', row[6], re.ASCII)
	tmp = df.at[i,"Text"].split()
	if(len(tmp)<=3):
		drop_list.append(i)

df = df.drop(df.index[drop_list]).reset_index(drop=True)
print("save to csv file")
df.to_csv(dir + "process/" + "process-" + file_name+".csv")

