from app.auth_util import build_client
from app.models import *
from app.search_by_title import article_2Youtube
from app.youtube_transcript import pull_transcript
from app.gga_edited import *
from app.youtubeUtil import parse_videoDetails, videos_list_multiple_ids




def search_articles1():
    now = datetime.datetime.now()
    client = build_client()
    # current_time = datetime.now()
    # two_weeks_ago = now - datetime.timedelta(days=1)
    counter = 0 
    while Article.query.filter(Article.searched == False).first():
        articles = Article.query.filter(Article.searched==False).limit(100) #NOT CLEANING BIG TIME WASTER
        articleIds = []
        for a in articles:
            articleIds.append(a.id)
        print(articleIds)
     
        for id_ in articleIds:
            A = Article.query.filter_by(id = id_).first()
            counter += 1
            title = A.title
            link = A.link
            aid= A.id
            body = A.body
            try:     
                print('')
                print(f"Searching youtube for '{title}' ")
                print('') 
                videoIds = article_2Youtube(client, title) #returns list of videoIds that match title 
                print(f"Of those, {len(videoIds)} are potential matches")
               
                vCount = 0
                for videoId in videoIds:
             
                    try:
                        print(videoId['videoId'])
                        transcript = pull_transcript(videoId['videoId'])
                        test = do_comparison(body, transcript)
                        vCount += 1
                        print(f'On {vCount} of {len(videoIds)}, test was {test}')
                        
                        if test == 'full match':
                            try:
                                response = videos_list_multiple_ids(client, part='snippet, statistics',id=videoId['videoId'])   
                            except Exception as e:
                                if 'credential' in str(e):   
                                    client = build_client()
                                    response = videos_list_multiple_ids(client, part='snippet, statistics',id=videoId['videoId'])  
                                else:
                                    print(e)
                                    raise ValueError 
                            transcript = parse_videoDetails(response, client, transcript)
                            link_article2video(videoId['videoId'], link)
                            mark_website_used(link)
                            print('ya yeet')
                            # print('fuckkckckckyeahhhahsdhash')
                        if test == 'something went wrong':
                            mark_videoManual(videoId, link)
                        if test == 'partial match':
                            mark_videoManual(videoId, link)
                            print('ill take it ')
                        print('')
                    # counter +=1
                    except Exception as e:
                        print(e)

                mark_article_searched(link)

            except Exception as e:
                if 'credential' in str(e):   
                    client = build_client()
                    search_articles1()     #implement rebuild sequence to reauthorize reques

                print(f"{e} reeeeee")
                # continue

        end = datetime.datetime.now()
        length = end - now  
        print(f"took {length} to process {counter} articles")

def link_article2video(videoId, article):
    V = Video.query.filter_by(videoId = videoId).first()
    A = Article.query.filter_by(link = article).first()
    # print(A.id)
    # var = A.id
    V.article_Id = A.id
    # var1 = V.id
    # print(V.id) 
    # A.video_Id = V.id
    db.session.commit()
    print(f"linked {videoId} with {article}")

def mark_website_used(url):
    domain = parse_url(url)
    W = Website.query.filter_by(base_url = domain).first()
    W.political_leaning = '1'
    A = Article.query.filter_by(link = url).first()
    A.website_Id = W.id
    db.session.commit()



def mark_videoManual(videoId, url):
    A = Article.query.filter_by(link = url).first()
    V = Video.query.filter_by(videoId = videoId).first()
    V.article_Id = A.id
    V.manual = True
    db.session.commit()