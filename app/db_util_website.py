from app import db
from app.models import Website, Article 
from sqlalchemy.exc import IntegrityError
import feedparser
from datetime import datetime



				
def send_article(title, description, link, ID):
	try:
		A = Article(link = link, searched = True, website_Id = WID)
		db.session.add(A)
		db.session.commit()

	except IntegrityError:
		db.session.rollback()


def find_article(link):
	A = Article.query.all() #filter_by(link = link).first()
	aids = []
	for a in A:
		if a.id is not None:
			aids.append(a.id)
			# return A.id
		else:
			raise ValueError
	print(len(aids)) 


def save_websiteInfo(d):  #actually used 
	'''
	Arguments: Takes dictionary of website info
	Function : Creates and adds website database entry 
	'''
	try:
		W = Website(base_url = d['Base_url'], name = d['Name'], description = d['Description'], \
				rss_url = d['Rss_url'], \
				origin = d['Origin'], domain_registered = d['Domain_registered'], \
				domain_updated= d['Domain_pulled'], political_leaning = d['use'])
		db.session.add(W)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		print('already added')
		# db.session.rollback()

def save_articleInfo(title, description, link, date, author, wid, body): #wid,
	try:
		A = Article(author = author, date_posted= date, \
			body = body, link = link, description= description, title = title, searched = False, last_search = datetime.now(), website_Id = wid)
		db.session.add(A)
		db.session.commit()
		print(f'Added article {link}')
	except IntegrityError:
		print(f'{link} already added ')
		db.session.rollback()


def update_articleInfo(title, description, link, date, author, wid, body): #wid,
	try:
		A = Article.query.filter_by(link = link).first()
		A.author = author
		A.date_posted= date
		A.body = body 
		A.link = link
		A.description= description 
		A.title = title 
		A.updated = True
		A.last_search = datetime.now()
		A.website_Id = wid
		db.session.commit()
		print(f'Added article {link}')
	except IntegrityError:
		print(f'{link} already added ')
		db.session.rollback()

def add_site(domain):
	try:
		W = Website(base_url = domain, political_leaning = 'check')
		db.session.add(W)
		db.session.commit()
		return True
	except IntegrityError:
		db.session.commit()
		W = Website.query.filter_by(base_url = domain).first()
		return W.id




def find_websiteModel(url):
	try:
		W = Website.query.filter_by(base_url = url).first()
		if W is not None:
			return W
		else: 
			# print(url)
			return None
	except Exception as e:
		print(e)

		

def give_articleNames():
    article_names = []
    A = Article.query.all()
    for a in A:
        article_names.append(a.title)
    return article_names

def update_websiteRSS(rss_url):
	pass

def	mark_article_searched(url):
	A = Article.query.filter_by(link = url).first()
	# A.last_search = datetime.now()
	A.searched = True
	db.session.commit()

# def updateArticles(data):
# 	total_articles = (len(data['items']))
# 		while item < total_articles:
# 			for item in items:
# 				title = data['items'][item]['title']
# 				description = data['items'][item]['description']
# 				link = data['items'][item]['link']
# 				data['items'][item]['title']

def add_DeadWebsite(url, feed):
	try:
		W = Webite(base_url = url, dead = True, feed = feed)
		db.session.add(W)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		W = Website.query.filter_by(base_url = url).first()
	
		