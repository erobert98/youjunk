import os
import sys
from app import db
from app.models import Channel, Video
from app.db_util import save_videoStats, save_videoInfo
import json
from app.youtube_transcript import *
from difflib import SequenceMatcher

def check_match(a,b):
    return SequenceMatcher(None, a, b).ratio()
# import google_auth_oauthlib.flow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google_auth_oauthlib.flow import InstalledAppFlow


# # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# # the OAuth 2.0 information for this application, including its client_id and
# # client_secret.
# CLIENT_SECRETS_FILE = "./client_secret.json"
# #C:/Users/emr673/PythonTest/Youtube/YouTool
# # This OAuth 2.0 access scope allows for full read/write access to the
# # authenticated user's account and requires requests to use an SSL connection.
# SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
# API_SERVICE_NAME = 'youtube'
# API_VERSION = 'v3'

    
# #migrate authentication to admin user login duh 

# def get_authenticated_service():
#   flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#   credentials = flow.run_local_server()
#   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
	print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
	resource = {}
	for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
		prop_array = p.split('.')
		ref = resource
		for pa in range(0, len(prop_array)):
			is_array = False
			key = prop_array[pa]

		# For properties that have array values, convert a name like
		# "snippet.tags[]" to snippet.tags, and set a flag to handle
		# the value as an array.
		if key[-2:] == '[]':
			key = key[0:len(key)-2:]
			is_array = True

		if pa == (len(prop_array) - 1):
		# Leave properties without values out of inserted resource.
			if properties[p]:
				if is_array:
					ref[key] = properties[p].split(',')
			else:
				ref[key] = properties[p]
		elif key not in ref:
		# For example, the property is "snippet.title", but the resource does
		# not yet have a "snippet" object. Create the snippet object here.
		# Setting "ref = ref[key]" means that in the next time through the
		# "for pa in range ..." loop, we will be setting a property in the
		# resource's "snippet" object.
			ref[key] = {}
			ref = ref[key]
		else:
		# For example, the property is "snippet.description", and the resource
		# already has a "snippet" object.
			ref = ref[key]
	return resource
resource = build_resource({
    'snippet.title': 'Sample playlist ',
    'snippet.description': 'This is a sample playlist description.',
    'snippet.tags[]': 'Python code, interactive',
    'snippet.defaultLanguage': '',
    'status.privacyStatus': 'private'})

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def channels_list_by_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.channels().list(
    **kwargs
  ).execute()

  # playlistID = response["items"][0]['contentDetails']["relatedPlaylists"]["uploads"]

  return response

def playlist_items_list_by_playlist_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().list(
    **kwargs
  ).execute()
    
  return response   

def videos_list_by_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()

  return response


def videos_list_multiple_ids(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()

  return response

def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()
  
  return response

def parse_channelInfo(response):
  # var =json.dumps(response)
  # response = StringIO(response)
  # response =  json.load(var)
  info = response['items'][0]
  # print(f"{info} and this is the test")
  cid = response['items'][0]['id']
  title = response["items"][0]["snippet"]["title"]
  description = response["items"][0]["snippet"]["description"]
  date = response["items"][0]["snippet"]["publishedAt"]
  playlistid = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
  channelviews = response["items"][0]['statistics']['viewCount']

  channel_details = {
    'Channelid' : cid,
    'Name' : title,
    'About' : description,
    'Date_joined' : date,
    'Playlistid' : playlistid,
    'Views' : channelviews,
    }
  return channel_details

def parse_videoDetails(response, client, transcript):
  '''
  Arguments : PlaylistItems List API Response 
  Function: Pulls relevant information and calls save_videoInfo


  '''
  length_list = len(response['items']) #could be a bug if zero?>
  # print(f"yooo {length_list}")
  item = 0
  while item < length_list:
      Channelid = response['items'][item]['snippet']['channelId']
      Videoid = response['items'][item]['id']
      # print(Videoid)
      Title = response['items'][item]['snippet']['title']
      Description = response['items'][item]['snippet']['description']
      try:
        likes = response['items'][item]['statistics']['likeCount']
      except KeyError:
        likes = 0
      try:
        dislikes = response['items'][item]['statistics']['dislikeCount']
      except:
        dislikes = 0
      try:
        views = response['items'][item]['statistics']['viewCount']
      except:
        views = 0
      try:
        comments = response['items'][item]['statistics']['commentCount']
      except:
        comments = 'No comments'
      # print(client)
      # transcript = pull_transcript(Videoid)
      # print(transcript)
      if 'disabled by uploader' in transcript:
        transcript = 'not available'
      # percent_match = check_match(title, Title) 
      # if percent_match > .70:
      Cresponse = channels_list_by_id(client, part='snippet,contentDetails,statistics',id=Channelid)        
      details = parse_channelInfo(Cresponse)  
      try:  
        # print(details)  
        sendingchannel = send_channel_info(details) 
        print(sendingchannel) 
      except Exception as e:  
        print('sfad') 
        raise e

      check = save_videoInfo(Videoid, Title, Description, Channelid, transcript, likes, dislikes, views, comments, aid)
      # print(f"saving video {Videoid} with {channel_id}")
      # channel_id?
        # var = True
      item += 1


def find_videoStats(video, client): 
  '''
  Arguments: Takes a list of videoIds with no stats 
  Returns: Updated Database entry with Stats 
  '''
  try:
    videoStats = videos_list_by_id(client, part='statistics',  id=video)
    stats = videoStats['items'][0]['statistics']
    return stats

  except:
    return None

  # Views = videoStats['items'][0]['statistics']['viewCount']
  # Likes = videoStats['items'][0]['statistics']['likeCount']
  # Dislikes = videoStats['items'][0]['statistics']['dislikeCount']
  # Favorites = videoStats['items'][0]['statistics']['favoriteCount']
  # Comments = videoStats['items'][0]['statistics']['commentCount']
 
  



# def run_file(channelId): #should be called scrape_new_channel  and need to implement nextpageToken
#   client = get_authenticated_service()
#   response = channels_list_by_id(client, part='snippet,contentDetails,statistics',id= channelId)  #returns playlist ID
#   channel_details = parse_channelInfo(response) #good
#   playlistID = channel_details['Playlistid']
#   # print(channel_details)
#   # print(playlistID)
#   channel = send_channel_info(channel_details) #fuck no
#   # if channel not None:
#   #   pass

#   video_details = playlist_items_list_by_playlist_id(client, part='snippet,contentDetails', maxResults=50, playlistId=playlistID) 
#   parse_videoDetails(video_details, client)
  # list_of_video = find_missingStats()
  # parse_listVideos(list_of_videos) #finish this




#   #create_channel(channelId, playlistId) #creates a new database entry for channel with playlistId
#   channel = find_channel(channelId, playlistId) #Ensures theres a corresponding Channel entry
#   video_list = playlist_items_list_by_playlist_id(client, part='snippet', maxResults=50, playlistId=playlistId) 
#   item = 0
#   list_of_videos = [] 
#   #reduce calls make a dict
#   while item < len(video_list['items']): #HELP
#       videoId = video_list['items'][item]['snippet']['resourceId']['videoId']
#       title = video_list['items'][item]['snippet']['title']
#       description = video_list['items'][item]['snippet']['description']
#       if not save_videoInfo(videoId, title, description, channelId):
#          #to do
#       list_of_videos.append(videoId)
#       #print(description)
#       item += 1
#   print(list_of_videos)
#   for video in list_of_videos:
#       videoStats = videos_list_by_id(client, part='statistics',  id=video)
#       stats = videoStats['items'][0]['statistics']
#       print(stats)
#       save_videoStats(video, stats)
        

# if __name__ == '__main__':
#     # When running locally, disable OAuthlib's HTTPs verification. When
#     # running in production *do not* leave this option enabled.
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
#     #channelId = sys.argv[1] #'UUzQUP1qoWDoEbmsQxvdjxgQ'  #
#     run_file('UCtcX0OObQQRC9XiU26P-V9A')#channelId)