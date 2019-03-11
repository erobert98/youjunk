from app import app
from app.db_util_website import *
from app.models import *
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from random import choice
from app.article_util import parse_url
from app.search_by_title import *



def fetch_results(search_term, number_results, start):
	article_title = search_term.replace(' ', '+').replace(':', '%3A').replace('(', '%28').replace('"', '%22').replace(')', '%29')
	google_url = f'https://www.google.com/search?q={article_title}&num={number_results}&start={start}'
	# proxy = {"http":"http://{}:{}@{}".format(username, password, PROXY_RACK_DNS)}
	# print('Proxy Below')
	# print(proxy)
	# print('URL Below')
	print(google_url)
	user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
	'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/537.11',
	'Mozilla/5.0 (Windows NT 6.0) yi; AppleWebKit/345667.12221 (KHTML, like Gecko) Chrome/23.0.1271.26 Safari/453667.1221',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2']
	
	s = requests.session()
	USER_AGENT = {'User-Agent': choice(user_agents)}
	response = s.get(google_url)  # proxies=proxy, headers = USER_AGENT)
	s.cookies.clear()
	# print(response.text)

	# response = session.get(google_url, headers=USER_AGENT)
	# response.raise_for_status()

	return search_term, response.text, start


def parse_results(html, keyword, start, CID, video_title, videoId):
	soup = BeautifulSoup(html, 'html.parser')

	found_results = []
	rank = 1 + start
	result_block = soup.find_all('div', attrs={'class': 'g'})
	for result in result_block:
		link = result.find('a', href=True)
		title = result.find('h3')
		description = result.find('span', attrs={'class': 'st'})
		if link and title:
			link = link['href']
			print(link)
			title = title.get_text()
			# ADD THE CHECK MATCH HERE 
			match = check_match(video_title, title)
			if match > .7:
				print('heck yes')
				# if description:
				# 	description = description.get_text()
				# if link != '#':
				# 	domain = parse_url(link)
				# 	WID =find_website(domain)
				# 	if WID is None:
				# 		status = add_site()
				# 		if status is True:
				# 			print(f'new site {domain}')
				# 			print(f'title: {title}, description: {description}, link: {link}')

				# 			send_article(title, link, WID)
				# 			link_article2video(videoId, link)
				# 			rank += 1
				# 			continue
				# 		if type(status) is int:
				# 			print('weird but ok')
				# 			send_article(title, link, WID)
				# 			link_article2video(videoId, link)

				# 			# rank += 1
				# 			continue
				# 	send_article(title, link, WID)
				# 	link_article2video(videoId, link)

				# 	print(f'title: {title}, description: {description}, link: {link}')
				# 	rank += 1
			else:
				continue
	return found_results

def find_ip(html):
	regex = r"(IP address: )(.*?)(?=<br>)"
	matches = re.search(regex, html, re.MULTILINE)
	# print(matches[2])
	return matches.group(2)

	
def scrape_google(search_term, number_results, CID, videoId):
	start = 0
	fail_count = 0
	finalResults = {}
	done = False
	while not done and fail_count < 15:   
		try:
			keyword, html, start = fetch_results(search_term, number_results, start)
			results = parse_results(html, keyword, start, CID, search_term, videoId)
			print(results)
			print('')
			print('!!!!!!!!!!!!!!!!!!!!!!')
			# ip = find_ip(html)
			# print(ip)
			if "CAPTCHA" in html: #tries again with same query
				fail_count += 1
				print(f'Got rate Limited for the {fail_count} time, we GO AGANE')
				print('')
				continue

			if "pnnext" not in html:  #sensitive, should implement better check but works
				done = True
				print('!!!!!!!!!!!!')
				print('Done Scraping')
				print('!!!!!!!!!!!!')
				continue

				
			print('!!!!!!!!!!!!!!!!!!!')
			print('SUCCESS')
			print('!!!!!!!!!!!!!!!!!!!')
			print(results)
			start += 100
		except Exception as e:
			# keyword, html, start = fetch_results(search_term, number_results, start)
			print('We Go Again but Why?')
			
			# start += 100
			print(e)
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		
	return finalResults, True



def main():
	# get_tor_session()
	Videos = Video.query.filter(Video.channel_Id is not None, Video.searched==False).limit(4)
	titles = [] 
	for video in Videos:
		tup_ = (video.title, video.channel_Id, video.id)
		titles.append(tup_)
	for title in titles[1:2]:
		try:
			# print(f'{title[0]}, {title[1]}')
			# break
			results, abort = scrape_google(title[0], 100, title[1], title[2])
			# for result in results:
				# send_result(result)
			if abort:
				break

		except Exception as e2:
			print(e2)
		finally:
			# sleep(10)
			pass

if __name__ == '__main__':
	main()
	
	
