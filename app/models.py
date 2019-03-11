from datetime import datetime
from app import db


class Channel(db.Model):
    __tablename__ = "channel"
    id = db.Column(db.Integer, primary_key=True)
    channelId = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    about = db.Column(db.Text)
    date_joined = db.Column(db.DateTime)
    playlistId = db.Column(db.String(100))
    views = db.Column(db.Integer)
    confirm = db.Column(db.Integer, default = 0)
    channel_type = db.Column(db.Text) #t2s , human, captions
    content_type = db.Column(db.Text) #political, left, right, what have u
    updated = db.Column(db.Boolean, default = False)
    searched = db.Column(db.Boolean, default = False)
    monetization = db.Column(db.Boolean, default = None)
    videos = db.relationship("Video")


    def __repr__(self):
        return '<Channel {}>'.format(self.channelId)

class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    views = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    videoId = db.Column(db.String(100), unique = True, nullable = False)
    channel_Id = db.Column(db.Integer, db.ForeignKey('channel.id'))  #something to do with foreign keys?    
    website_Id = db.Column(db.Integer, db.ForeignKey('website.id'))
    article_Id = db.Column(db.Integer, db.ForeignKey('article.id')) #will this handle multiple articleIds values
    needs_stats = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean, default = False)
    transcript = db.Column(db.Text)
    manual = db.Column(db.Boolean, default = False)
    searched = db.Column(db.Boolean, default = False)
    monetization = db.Column(db.Boolean, default = None)
    # channel = db.relationship("Channel")
    # article = db.relationship("Article")
    def __repr__(self):
        return '<Video {}>'.format(self.videoId)

class Article(db.Model):
    __tablename__="article"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text)
    link = db.Column(db.Text, unique = True, nullable=False)
    date_posted = db.Column(db.Text)
    body = db.Column(db.Text)
    description = db.Column(db.Text)
    title = db.Column(db.Text)
    website_Id = db.Column(db.Integer, db.ForeignKey('website.id')) #is this a problem with website_id in video
    # video_Id = db.Column(db.Integer, db.ForeignKey('video.id')) 
    searched = db.Column(db.Boolean)
    last_search = db.Column(db.DateTime, default=datetime.now())
    # website = db.relationship("Website")  
    searched = db.Column(db.Boolean, default = False)
    updated = db.Column(db.Boolean, default = False)
    video = db.relationship("Video")

class Website(db.Model):
    __tablename__ = "website"
    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    rss_url = db.Column(db.String(100)) 
    political_leaning = db.Column(db.String(100))
    alexa_ranking = db.Column(db.Integer)
    origin = db.Column(db.Text) #
    domain_registered = db.Column(db.String(100))
    domain_updated = db.Column(db.String(100)) #
    generator = db.Column(db.String(120)) #
    full_rss = db.Column(db.Text)
    dead = db.Column(db.Boolean)
    article = db.relationship("Article")
    video =db.relationship("Video")



