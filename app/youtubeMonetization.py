from bs4 import BeautifulSoup
import requests
from random import choice
from app.models import *
import time

def pull_videoIds(): 
	C = Channel.query.filter_by(confirm = 0).all()
	clist = []
	for c in C:
		clist.append(c)

	channelArticles = {}
	item = 0
	for channel in clist:
		item += 1
		vlist = []
		for video in channel.videos:
			vlist.append(video.videoId)
		channelArticles[item] = vlist 

	# print(len(channelArticles))
	return channelArticles



	

def is_monetized(channelArticles):
	results = {}
	for channel, list_videos in channelArticles.items():
		money = 0
		political = 0
		L = 3
		num_vids = len(list_videos[0:L])
		print(channel)
		# time.sleep(8)
		for videoid in list_videos[0:L]:
			# print(videoid)
			# break
			# videoid = d[videoids] 
			s = requests.session()
			print(f'Starting Analysis of {videoid}')
			url = 'https://www.youtube.com/watch?v=' + videoid
			result = s.get(url)
			soup = BeautifulSoup(result.content, 'html.parser')
			soups = str(soup)
			if 'googleads.g.doubleclick.net' in soups:
				print(f'{videoid} THIS HAS ADS ')
				money += 1
				# return True
				# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
			elif 'googleadservices.com' in soups:
				print(f'{videoid} THIS HAS ADS ')
				money += 1
				# return True
				# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
			else:
				political +=  1
				if videoid == 'aI8OdsSRrWY':
					print('~~~~~~~~~~~~~~')
					print(soups)
					# break
				print(f'{videoid} DOES NOT HAVE ADS ')
				print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		if money > num_vids/2  :
			results[channel] = 1
		if money < num_vids/2:
			results[channel] = 0


			# return False
	# print(f"Money : {money}  Political : {political}")
	print(results)

def main():
	videoIds = pull_videoIds()
	is_monetized(videoIds) 
	# username = "niccdias"
	# password = "bM65lMa99ybZcd0r"
	# PROXY_RACK_DNS = "megaproxy.rotating.proxyrack.net:222"

	
	# user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	# 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	# 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
	# 'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	# 'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	# 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
	# 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
	# 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
	# 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	# 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	# 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
	# 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
	# 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/537.11',
	# 'Mozilla/5.0 (Windows NT 6.0) yi; AppleWebKit/345667.12221 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/453667.1221',
	# 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
	# 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
	# 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2']
	# proxy = {"http":"http://{}:{}@{}".format(username, password, PROXY_RACK_DNS)}
	# print('Proxy Below')
	# print(proxy)
	# USER_AGENT = {'User-Agent': choice(user_agents)}
