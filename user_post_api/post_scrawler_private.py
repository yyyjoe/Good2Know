import json
import os.path
import logging
import argparse
import pandas as pd
try:
	from instagram_private_api import (Client, __version__ as client_version)
except ImportError:
	import sys
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
	from instagram_private_api import (
		Client, __version__ as client_version)

"""
Retrieve posts:
input: posts(list)
output: text_list(list)
"""
def process_posts(posts):
	text_list = []
	if len(posts) == 0:
		return []
	for post in posts:
		if not post['caption'] or not post['caption']['text']:
			continue
		text_list.append(post['caption']['text'])

	return text_list

def main():
	logging.basicConfig()
	logger = logging.getLogger('instagram_private_api')
	logger.setLevel(logging.WARNING)

	# Example command:
	parser = argparse.ArgumentParser(description='Data Mining Final Project')
	parser.add_argument('-i', '--inputfile', dest='inputfile', type=str, required=True)
	parser.add_argument('-o', '--outputfile', dest='outputfile', type=str, required=True)
	parser.add_argument('-u', '--username', dest='username', type=str, required=True)
	parser.add_argument('-p', '--password', dest='password', type=str, required=True)
	parser.add_argument('-debug', '--debug', action='store_true')

	args = parser.parse_args()
	if args.debug:
		logger.setLevel(logging.DEBUG)

	print('Client version: {0!s}'.format(client_version))
	api = Client(args.username, args.password)

	df = pd.read_csv(args.inputfile)

	# output data frame
	# new_df = pd.DataFrame(columns = ['user_name', 'user_id', 'caption', 'link'])
	new_df = pd.DataFrame(columns = ['user_name', 'caption'])

	for index, row in df.iterrows():
		text_list = []
		results = api.username_feed(row['user_name'])
		text_list += process_posts(results['items'])
		next_max_id = results.get('next_max_id')
		while next_max_id:
			results = api.username_feed(row['user_name'], max_id=next_max_id)
			text_list += process_posts(results['items'])
			next_max_id = results.get('next_max_id')
		new_df = new_df.append({'user_name': row['user_name'], 'text': '\n'.join(text_list)}, ignore_index=True)
		break

	# print(len(text_list))
	new_df.to_csv(args.outputfile)


if __name__ == "__main__":
	main()
	