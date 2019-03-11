from app.db_util import *
from app.youtubeUtil import *
from app.auth_util import *
from app.db_util_website import *
import json
from app import db, app
from app.models import Video, Channel, Website, Article
import re
from difflib import SequenceMatcher

def check_match(a,b):
    return SequenceMatcher(None, a, b).ratio()

def video_articleMatcher():
	matches = {}
	V = Video.query.all()
	A = Article.query.all()
	# print(V)
	for v in V:
		# print(v.title)
		for a in A:
			ok = check_match(v.title, a.title)
			print(ok)
			if ok > .8:
				# print(a.link)
				matches[v.id] = a.id
				# v.website_Id = find_website(a.url)
				# db.session.commit()
				test_grace(v.id, a.id) 
				print(matches)
				continue





def find_correspondingVideo():
	
	videoTitles = give_videoNames()
	# print(videoTitles)
	client = build_client()
	for title in videoTitles:
		print(f'searching for {title}')
		videoDetails =search_list_by_keyword(client,
		    part='snippet',
		    maxResults=50,
		    q=title,
		    type='video')
		# print(len(videoDetails['items']))
		item = 0
		items = number_ofResults(videoDetails)
		print(items)
		if items is not 0:
			while item < items:
				# print(videoId)
				videoId= videoDetails['items'][item]['id']['videoId']
				# print(videoId)
				cid = save_videoId(videoId, videoDetails, item)
				add_missing_channel(cid)
				item += 1


def article_2Youtube(client,title):
	# titles = give_articleNames()  
	#input article link and search youtube for the title if match, save video and article 
	# client = get_authenticated_service()
	# for title in titles:
	# print(f'searching for {title}')
	videoDetails =search_list_by_keyword(client,
	    part='snippet',
	    maxResults=50,
	    q=title,
	    type='video')
	# print(len(videoDetails['items']))
	item = 0
	items = number_ofResults(videoDetails)  #len(videoDetails)
	# print(items)
	matches = []
	print(f"There are {items} results from that {title} Search")
	# print(videoDetails)
	if items is not 0:
		while item < items:
			Vtitle = videoDetails['items'][item]['snippet']['title']
			similarity = check_match(Vtitle, title)
			# print(Vtitle)
			if similarity > .6:
				# print('success')
				match = []
				# print(f'similar enough match between {Vtitle} and {title}')
				videoId= videoDetails['items'][item]['id']['videoId']
				cname = videoDetails['items'][item]['snippet']['channelTitle']
				vdescription = videoDetails['items'][item]['snippet']['description']
				dict_ = {'videoId' : videoId, 'cname' : cname, 'vdescription': vdescription}
				# print(dict_)
				# print(dict_['videoId'])
				# print('heydksadjsadjas')
				matches.append(dict_)
				item += 1
			else:	
				item += 1
	# print(matches)
				# cid = data['items'][item]['snippet']['channelId']	
				# print(videoId)
				# add_missing_channel(cid)
				# save_videoId(videoId, videoDetails, item)
	# print(matches)
	return matches

def add_missing_channel(cid):
	channel = find_channel(cid)
	if channel is None:
		print('check')
		response = channels_list_by_id(client, part='snippet,contentDetails,statistics',id= cid)  #returns playlist ID
		channel_details = parse_channelInfo(response)
		send_channel_info(channel_details)
		print(f'added {cid}')

def number_ofResults(videoDetails):
	videoDetails = json.dumps(videoDetails)
	regex = r"youtube#searchResult"
	matches = re.findall(regex, videoDetails, re.MULTILINE)
	return len(matches)
		