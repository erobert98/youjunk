from app.youtubeUtil import *
from app.db_util import *
from app.auth_util import *
from app.youtube_transcript import *


def add_channelVideos(): #should be called scrape_new_channel  and need to implement nextpageToken
  client = build_client()  #estaiblish connection to google api
  counter = 1
  while Channel.query.filter_by(updated_videos = False).first():   #ensures theres stil channels to be updated
    channels = Channel.query.filter_by(updated_videos = False).limit(5) #selects 5 to work on 
    c_list = []
    for c in channels:
      c_list.append(c.id)
    print(c_list)               #create list of channel IDs to work on to avoid missing models
    for id_ in c_list:
      try:
        chan = Channel.query.filter_by(id = id_).first()
        cid = chan.id 
        pid = chan.playlistId
        try:
          video_details = playlist_items_list_by_playlist_id(client, part='snippet,contentDetails', maxResults=50, playlistId=pid) 
        except Exception as e: #Re-establishes connection to api in case of credential expiring
          if 'credential' in str(e):   
              client = build_client()
              video_details = playlist_items_list_by_playlist_id(client, part='snippet,contentDetails', maxResults=50, playlistId=pid) 
          else:
            print(e)  #this shouldnt ever really happen, probably not a good idea to have a valueerror here
            raise ValueError
        update_channel_videos(video_details)
        mark_channel_updated(cid) #marked updated videos true.
      except Exception as e:
        if 'credentials' in str(e):
          client =  build_client()  #this one shouldnt ever be called but u never know 
          add_channel()    #calls again in case it messes up
    print('moving on')  
    
  
def update_channel_videos(response):
  # print(response)
  length_list = len(response['items']) #could be a bug if zero?>
  # print(f"yooo {length_list}")
  item = 0
  while item < length_list:
    try:
      Channelid = response['items'][item]['snippet']['channelId']
      Videoid = response['items'][item]['contentDetails']['videoId']
      print(Videoid)
      transcript = pull_transcript(Videoid)
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
        comments = 0
      check = update_channelVideos(Videoid, Title, Description, Channelid, transcript, likes, dislikes, views, comments)
      # print('heck yeh')
      item += 1
    except Exception as e:
      print(e)
      item += 1