from app.db_util_website import *
import datetime
import json
from bs4 import BeautifulSoup as parser







def add_websiteInfo(url, feed):   #add field for sites when they have a vid
	# domain_registered= get_domainInfo(url)
	try:
		# full_feed = json.dumps(feedparser.parse(feed))
		domain_registered = str(datetime.datetime.now())
		details = pull_websiteData(feed)
		details['Base_url'] = url
		details['Rss_url'] = feed
		details['Domain_registered'] = domain_registered
		details['Origin'] = 'crowdtangle'
		details['Domain_pulled'] = str(datetime.datetime.now())
		details['Alexa_ranking'] ='tbd'
		details['use'] = '0'
		# details['Full_feed'] = full_feed

		# print(details)
		save_websiteInfo(details)
		# parse_websiteArticles(feed, details['Base_url'])
	except Exception as e:
		print(e)
		print(f'bet its a bad {domain} on link {url}')
		add_DeadWebsite(url, feed)
		 




def pull_websiteData(URL):
	try:
		try:
			data = feedparser.parse(URL)
			try:
				name = data['feed']['title']
			except:
				name = URL
			try:
				generator = data['feed']['generator']
				pass
			except:
				generator = 'N/A'
			description = data['feed']['description']
		except Exception as e:
			description = 'Website failed feedparser to find some site stats'
			name = 'Website failed feedparser to find some site stats'
			generator = 'Website failed feedparser to find some site stats'

		website_details = {
			'Full_rss' : data,
			'Name' : name,
			'Generator' : generator,
			'Description' : description
		}
	except:
		website_details = {}

	return website_details
	



#