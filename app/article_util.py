from app.db_util_website import *
import csv
from urllib.parse import urlparse
import re
from newspaper import Article as NA



def parse_url(url):
	# for url in urls:
	parsed_uri = urlparse(url)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	if 'http:/' in result:
		result = result.replace('http', 'https')
		return result
	else: 
		return result

def fresh_parse_article(url, wid):
	# print(url)
	if  "'" in url:
		try:
			url = url.replace("'", "%E2%80%99")
		except Exception as e:
			print(e)
	article = NA(url)
	article.download()
	article.parse()	
	article.nlp()
	body = article.text 
	description = article.summary
	date = article.publish_date	
	author = str(article.authors)
	title = article.title
	domain = parse_url(url)
	
	update_articleInfo(title, description, url, date, author, wid, body)

def parse_article(url, domain):
	print(url)
	if  "'" in url:
		try:
			url = url.replace("'", "%E2%80%99")
		except Exception as e:
			print(e)

	# url = str(url)
	# regex = "\['(.....*)\'\]"
	# matches = re.findall(regex, url, re.MULTILINE)
	# print(f" this is the regex match {matches[0]}")
	# nice_url = matches[0]
	article = NA(url)
	article.download()
	article.parse()	
	article.nlp()
	body = article.text 
	description = article.summary
	date = article.publish_date	
	author = str(article.authors)
	title = article.title
	# domain = parse_url(url)
	feed = domain + 'feed'
	wid = find_website(domain)
	note = 'from crowdtangle '
	if wid is None:
		# print(feed)
		try:
			add_websiteInfo(domain, feed)
			wid = find_website(domain)
			print('new domain added')
		except:
			print(f"{domain} not added")
	save_articleInfo(title, description, url, date, author, wid, body)

