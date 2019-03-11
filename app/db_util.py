from app import db
from app.models import Video, Channel, Article, Website
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct
from app.add_website import *
from app.article_util import *

def delete_duplicateArticles():
    A = Article.query.filter_by(searched = False).all()
    for a in A:
        db.session.delete(a)
        db.session.commit()


def addusedDomains():
    AIDS = []
    channels = Channel.query.all()
    for channel in channels:
        for video in channel.videos:
            if video.article_Id not in AIDS:
                AIDS.append(video.article_Id)

    Alinks = []
    for aid in AIDS:
        article = Article.query.filter_by(id = aid).first()
        # var = (aid , article_link)
        Alinks.append(article.link)

    websites = []
    for link in Alinks:
        url = parse_url(link)
        feed = url + 'feed'
        var = (url, feed)
        if var not in websites:
            websites.append(var)
    # print(websites)
    # raise ValueError    


    for website in websites:
        # print(website[0])
        try:
            add_websiteInfo(website[0], website[1])
            # W = find_websiteModel(website[0])
            # W.political_leaning = '1'
            # db.session.commit()

        except Exception as e:
            print(e)
            pass
    
def linkarticles2Domains():
    A = Article.query.filter_by(website_Id = None).limit(3000).all()
    for a in A:
        try:
            domain = parse_url(a.link)
            print(domain)
            W = Website.query.filter_by(base_url = domain).first()
            print(a.title)
            # print(W.base_url)
            a.website_Id = W.id
            W.article_Id = a.id
            db.session.commit()
            print(f"Linking {a.link} with {W.base_url} using {domain} as base_url ")
        except Exception as e:
            print(e)

def subtitle_channel1(CID):
    C = Channel.query.filter_by(id = CID).first()
    C.channel_type = 'Captions'
    C.confirm = 2
    db.session.commit()
def human_channel1(CID):
    C = Channel.query.filter_by(id = CID).first()
    C.channel_type = 'Human Read'
    C.confirm = 2
    db.session.commit()

def confirm_channel(CID):
    C = Channel.query.filter_by(id = CID).first()
    C.channel_type = 'Computer Generated Voice'
    C.confirm = 2
    db.session.commit()
def not_channel1(CID):
    C = Channel.query.filter_by(id = CID).first()
    C.channel_type = 'Not Notable'
    C.confirm = 1
    db.session.commit()
def null_channel1(CID):
    C = Channel.query.filter_by(id = CID).first()
    C.confirm = None
    db.session.commit()


def find_channel(channelID):
    try:
        C = Channel.query.filter_by(channelId = channelID).first()
        return C.id
    except Exception as e:
        print(e)

# find_channel(ChannelID)

def save_videoInfo(VideoID, Title, Description, ChannelID, transcript, likes, dislikes, views, comments):  #should this  call the function that pulls STATS
    '''
      Arguments : Takes video details
      Function: Creates database entry 

    '''
    try:
        cid = find_channel(ChannelID)
    except: 
        cid = ChannelID
        # raise ValueError('save_videoInfo not malleable')
    try:
        V = Video(channel_Id = cid, videoId = VideoID, title = Title, searched = True,description = Description, needs_stats = True, transcript = transcript, dislikes = dislikes, likes = likes, views = views , comments = comments)
        db.session.add(V)
        db.session.commit()
        return True
    except IntegrityError:
        print('already added')
        db.session.rollback()
        return False

def update_channelVideos(VideoID, Title, Description, ChannelID, transcript, likes, dislikes, views, comments):
    try:
        C = Channel.query.filter_by(channelId = ChannelID).first()
        cid = C.id
        V = Video.query.filter_by(videoId = VideoID).first()
        V.title = Title
        V.description = Description
        V.channel_Id = cid
        V.transcript = transcript
        V.likes = likes
        V.dislikes = dislikes
        V.Views = views
        V.comments = comments 
        V.searched = False  
        print('')
        db.session.commit()
        print(f'Updated video {VideoID}')

    except Exception as e:
        if save_videoInfo(VideoID, Title, Description, ChannelID, transcript, likes, dislikes, views, comments):
            print(f'added video {VideoID}')
        

def save_videoStats(video, stats):
    '''
    Arguments : Takes a Videoid and stats api response 
    Function : Finds corresponding database entry 
    Returns : updated database entry for videoId 

    '''

    try:
        V = find_videoIDs(video)
        try:
            V.views = stats['viewCount']
        except:
            pass
        try:
            V.likes = stats['likeCount']
        except:
            pass
        try:
            V.dislikes = stats['dislikeCount']
        except:
            pass
        try:
            V.favorites = stats['favoriteCount']
        except: 
            pass
        V.needs_stats = False
        try:
            V.comments = stats['commentCount']
        except:
            pass
        db.session.commit()
        pass
    except IntegrityError:
        print('already has stat information')

def mark_channel_updated(cid):
    C = Channel.query.filter_by(id = cid).first()
    C.updated_videos = True
    db.session.commit()
    
def send_channel_info(channel_details):
    '''
    Arguments : Relevant Channel information 
    Function : Creates database entries
    Returns : Returns False if channel already exists

    '''


    try:
        C = Channel(channelId = channel_details['Channelid'], name = channel_details['Name'], about = channel_details['About'], playlistId = channel_details['Playlistid'], views = channel_details['Views'])
        db.session.add(C)
        db.session.commit()
        return 'Added channel'
        
    except IntegrityError:
        db.session.rollback()
        return 'Channel already in DB'
   

def find_videoIDs(videoID):
    V = Video.query.filter_by(videoId = videoID).first()
    return V

def give_videoNames():
    video_names = []
    V = Video.query.all()
    for v in V:
        video_names.append(v.title)
    return video_names

def save_videoId(videoId, data, item): #add need channel
    Title =data['items'][item]['snippet']['title'] 
    cid = data['items'][item]['snippet']['channelId']
    print(f'saving video {videoId} with {Title}')
    CID = find_channel(cid)
    try:
        V = Video(videoId = videoId, channel_Id = CID, \
            needs_stats = True, title = data['items'][item]['snippet']['title'])
        db.session.add(V)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f' {e} already added : {videoId}  {Title}')
    return cid


def find_missingStats(): 
    V = Video.query.filter_by(needs_stats = True).first()
    if V:
        return V.videoId


def find_missingChannels():
    V = Video.query.filter_by(needs_channel = True).first()
    if V:
        return V.videoId

def mark_videoDeleted(videoId):
    V = Video.query.filter_by(videoId = videoId).first()
    V.deleted = True
    V.needs_stats = False
    db.session.commit()

def mark_videoManual(videoId, url):
    A = Article.query.filter_by(link = url).first()
    V = Video.query.filter_by(videoId = videoId).first()
    V.article_Id = A.id
    V.manual = True
    db.session.commit()


def add_link(link):
    try:
        A = Article(link = link, searched = False)
        db.session.add(A)
        db.session.commit()
        print(f'added {link}')
    except Exception as e:
        db.session.rollback()
        # print(e)
        # print(e)
    