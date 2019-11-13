import json
import os.path
import logging
import argparse
import pandas as pd
import hashlib
import string
import random
import re
from langdetect import detect
from instagram_web_api import Client as webClient

try:
	from instagram_private_api import (Client, __version__ as client_version)
except ImportError:
	import sys
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
	from instagram_private_api import (
		Client, __version__ as client_version)



class MyClient(webClient):
	@staticmethod
	def _extract_rhx_gis(html):
		options = string.ascii_lowercase + string.digits
		text = ''.join([random.choice(options) for _ in range(8)])
		return hashlib.md5(text.encode())

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
		lang = None
		try:
			lang = detect(post['caption']['text'])
		except:
			continue
			# print('This text cannot be differentiated.')

		# text_list.append(re.sub(r'[^a-zA-Z]+', ' ', post['caption']['text'], re.ASCII))
		if lang == 'en':
			text_list.append(post['caption']['text'])

	return text_list

def main():
	# web_api (w/o authentication)
	web_api = MyClient(auto_patch=True, drop_incompat_keys=False)

	# app_api (w/ authentication)
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
	new_df = pd.DataFrame(columns = ['user_id', 'user_name', 'text'])
	
	process_bar = [0, 0.25, 0.5, 0.75, 1]

	for index, row in df.iterrows():
		process_rate = 0
		process_idx = 0

		# get user info
		user_info = None
		try:
			user_info = web_api.user_info2(row['user_name'])
		except:
			print('username: ' + row['user_name'] + ' is invalid.')
			continue
		if not user_info:
			continue

		user_id = user_info['id']
		user_post_count = user_info['counts']['media']		

		text_list = []
		results = api.username_feed(row['user_name'])
		text_list += process_posts(results['items'])
		next_max_id = results.get('next_max_id')

		while next_max_id:
			if len(text_list) / user_post_count > process_bar[process_idx]:
				print('Processing username = "' + row['user_name'] + '" '+ '%.2f' % (100 * len(text_list) / user_post_count) + '%')
				process_idx += 1
			results = api.username_feed(row['user_name'], max_id=next_max_id)
			text_list += process_posts(results['items'])
			next_max_id = results.get('next_max_id')

		print('Processing username = "' + row['user_name'] + '" '+ '%.2f' % (100 * len(text_list) / user_post_count) + '%')
		
		new_df = new_df.append({'user_id': user_id, 'user_name': row['user_name'], 'text': '\n'.join(text_list)}, ignore_index=True)
		# break

	new_df.to_csv(args.outputfile)


if __name__ == "__main__":
	main()
	