import json
import os.path
import argparse
import pandas as pd
import hashlib
import string
import random
import re
from langdetect import detect
from instagram_web_api import Client as webClient


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

		if lang == 'en':
			text_list.append(post['caption']['text'])

	return text_list

def process_text(text):
	lang = None
	try:
		lang = detect(text)
	except:
		print('This text cannot be differentiated.')
		
	if lang == 'en':
		return text
	else:
		return ''

def main():
	# web_api (w/o authentication)
	web_api = MyClient(auto_patch=True, drop_incompat_keys=False)
	
	# Example command:
	parser = argparse.ArgumentParser(description='Data Mining Final Project')
	parser.add_argument('-i', '--inputfile', dest='inputfile', type=str, required=True)
	parser.add_argument('-o', '--outputfile', dest='outputfile', type=str, required=True)
	parser.add_argument('-p', '--postcount', dest='postcount', type=str, required=True)

	args = parser.parse_args()
	df = pd.read_csv(args.inputfile)
	
	# output data frame
	new_df = pd.DataFrame(columns = ['user_id', 'user_name', 'user_img_url', 'followed_by', 'post_count',  'text'])
	
	for index, row in df.iterrows():
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
		followed_by_count = user_info['counts']['followed_by']
		user_img_url = user_info['profile_picture']

		user_feed_info = web_api.user_feed(user_id, count=min(20, user_post_count))

		index = 0
		text_list = []
		for post in user_feed_info:
			caption = process_text(post['node']['caption']['text'])
			if len(caption) > 0:
				index += 1
				text_list.append(caption)
			if index >= int(args.postcount):
				break
		new_df = new_df.append({'user_id': user_id, 'user_name': row['user_name'], 'user_img_url': user_img_url, 'followed_by': followed_by_count, 'post_count': user_post_count, 'text': '\n'.join(text_list)}, ignore_index=True)


	emoji_pattern = re.compile(u"(["                     # .* removed
u"\U0001F600-\U0001F64F"  # emoticons
u"\U0001F300-\U0001F5FF"  # symbols & pictographs
u"\U0001F680-\U0001F6FF"  # transport & map symbols
u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                "])", flags= re.UNICODE) 

	for index, row in new_df.iterrows():
		row['text'] = re.sub(r'[^a-zA-Z]+', ' ', row['text'], re.ASCII)
		row['text'] = emoji_pattern.sub(u'', row['text'])


	new_df.to_csv(args.outputfile)

if __name__ == "__main__":
	main()
	