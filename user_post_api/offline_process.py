import json
import os.path
import argparse
import pandas as pd
import random
import re

"""
Only used for offline post filtering
"""
def main():

	parser = argparse.ArgumentParser(description='Data Mining Final Project')
	parser.add_argument('-i', '--inputfile', dest='inputfile', type=str, required=True)
	parser.add_argument('-o', '--outputfile', dest='outputfile', type=str, required=True)
	args = parser.parse_args()

	emoji_pattern = re.compile(u"(["                     # .* removed
u"\U0001F600-\U0001F64F"  # emoticons
u"\U0001F300-\U0001F5FF"  # symbols & pictographs
u"\U0001F680-\U0001F6FF"  # transport & map symbols
u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                "])", flags= re.UNICODE) 

	df = pd.read_csv(args.inputfile)
	for index, row in df.iterrows():
		row['text'] = re.sub(r'[^a-zA-Z]+', ' ', row['text'], re.ASCII)
		row['text'] = emoji_pattern.sub(u'', row['text'])


	df.to_csv(args.outputfile)


if __name__ == "__main__":
	main()
	