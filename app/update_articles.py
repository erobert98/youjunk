from app.add_website import add_websiteInfo, pull_websiteData
from app.db_util_website import mark_article_searched
from app.article_util import fresh_parse_article


def update_articles1(): #convert to find articles where they a) have article.id and b) 
    
    while Article.query.filter(Article.updated==False).first():
        dead_domains = find_dead_domains()
        articles = Article.query.filter(Article.updated == False).limit(100) #NOT CLEANING BIG TIME WASTER
        # print(articles)
        articleIds = []
        for a in articles:
            # print('uh')
            articleIds.append(a.id)
        print(articleIds)
        for id_ in articleIds:
            A = Article.query.filter_by(id =id_).first()
            url = A.link
            print(f'working on {url}')
            domain = parse_url(url)
            # print('what')
            feed = domain + 'feed'
            if domain in dead_domains:
                mark_article_searched(url)
                mark_article_updated(url)
                print(f'{domain} is a dead domain')
                continue
            if 'video.twimg.com' in url:
                mark_article_searched(url)
                print(f'{domain} is a dead domain')
                continue
            wid = find_website(domain)
            if wid is None:
                # print(feed)
                try:    
                    add_websiteInfo(domain, feed)
                    W = find_websiteModel(domain)
                    wdead = W.dead
                    if wdead is False or None:
                        print(f'new domain added : {domain}')
                    else:
                        mark_article_searched(url)
                        print(f'dead link {domain}')
                        continue
                except Exception as e:
                    print(e)
                    print(f"{domain} not added")
            if wid is not None:
                try:
                    fresh_parse_article(url, wid)
                    print(f'{url} updated')
                    # counter += 1
                except Exception as e:
                    if 'HTTPSConnectionPool' in str(e):
                        # insecure_connection()
                        A.searched = True
                        W = find_websiteModel(domain)
                        W.dead = True
                        dead_domains.append(W.base_url)
                        db.session.commit()
                        print(f'{domain} is slow/unusable')
                    if 'Client Error' or '503 Server Error' in str(e):
                        # insecure_connection()
                        A.searched = True
                        db.session.commit()
                        print(f'{url} is down/unreachable')
                    else:
                        print(e)
            mark_article_updated(url)


def find_dead_domains():  #returns list of dead domains
    W = Website.query.filter_by(dead = True).all()
    list_ = []
    for w in W:
        list_.append(w.base_url)

    return list_

def mark_article_updated(url):
    try:
        A = Article.query.filter_by(link = url).first()
        A.updated = False
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def find_website(url):  #returns entrys id based on url
    try:
        W = Website.query.filter_by(base_url = url).first()
        if W is not None:
            return W.id
        else: 
            return None
    except Exception as e:
        print(e)




def find_websiteModel(url):  #return the full model
    try:
        W = Website.query.filter_by(base_url = url).first()
        if W is not None:
            return W
        else: 
            # print(url)
            return None
    except Exception as e:
        print(e)

