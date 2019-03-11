from flask import render_template, flash, redirect, url_for, session, request
from app import app, db
from app.models import Channel, Video, Channel, Video
from app.forms import *
import math
from app.add_channelVideos import add_channelVideos
import httplib2
import datetime
# from config import Auth
from urllib.error import HTTPError
import json
from app.db_util import *
from app.search_articles import *
from sqlalchemy import cast, func, asc, desc
from app.add_rawLinks import *
from app.update_articles import *
from app.search_articles import *
from app.add_channelVideos import *


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/channel/<channel_Id>', methods = ['GET', 'POST'])
def displaychannel(channel_Id):
  C = Channel.query.filter_by(id = channel_Id).first()
  return render_template('displaychannel.html', C = C)


@app.route('/channelvideos')
def channelvideos():
  add_channelVideos()
  return render_template('index.html')

@app.route('/rollback', methods=['GET', 'POST'])
def rollback():
    rollback1()
    return render_template('index.html')

@app.route('/search_articles', methods=['GET', 'POST'])
def search_articles():
    form = ProcessFilesForm()
    process = 'search articles for videos'
    if form.validate_on_submit():
        search_articles1()
        return render_template('index.html')
    return render_template('process_files.html', form = form, process = process)

@app.route('/add_articles', methods=['GET', 'POST'])
def adding_articles():
    form = ProcessFilesForm()
    process = 'add articles from CSV'
    if form.validate_on_submit():
        add_from_csv('./articles.csv')
        return render_template('index.html')
    return render_template('process_files.html', form = form, process = process)

@app.route('/update_articles', methods = ['GET', 'POST'])
def update_articles():
    form = ProcessFilesForm()
    process = 'fill article entries'
    if form.validate_on_submit():
        update_articles1()
    return render_template('process_files.html', form = form, process = process)



@app.route('/domains', methods=['GET', 'POST'])
def domains():
    page = request.args.get('page', 1, type=int)
    websites = Website.query.filter_by(political_leaning = '1').paginate(page, 10, False)
    W = Website.query.filter_by(political_leaning = '1').count()
    last_page = math.ceil(int(W) / int(10))
    print(last_page)
    page_url = "url_for('domains', page="
    next_url = url_for('domains', page=websites.next_num) \
      if websites.has_next else None
    prev_url = url_for('domains', page=websites.prev_num) \
      if websites.has_prev else None

    return render_template('domains.html', confirmed_websites = W, websites = websites.items, cols =['URL','Name','Article Titles'], page = page, next_url=next_url, prev_url=prev_url, last_page=last_page)


@app.route('/channels', methods=['GET', 'POST'])
def channels():
    page = request.args.get('page', 1, type=int)
    # channels = Channel.query.order_by(Channel.id.asc()).paginate(page, 10, False)
    channels = Channel.query.filter_by(confirm = 2).order_by(Channel.views.desc()).paginate(page, 10, False)
    C = Channel.query.filter_by(confirm = 2).count()
    last_page = math.ceil(int(C) / int(10))
    print(last_page)
    cviews = Channel.query.filter_by(confirm = 2).all()
    cviewsCount = Channel.query.filter_by(confirm = 2).count()
    views = []
    for c in cviews:
      views.append(c.views)
    # print(channels.videos)
    # print(videos)
    total_views = sum(views)
    page_url = "url_for('allresults', page="
    next_url = url_for('channels', page=channels.next_num) \
      if channels.has_next else None
    prev_url = url_for('channels', page=channels.prev_num) \
      if channels.has_prev else None
    Computer = Channel.query.filter_by(channel_type ='Computer Generated Voice').count()
    Captions = Channel.query.filter_by(channel_type ='Captions').count()
    Human  = Channel.query.filter_by(channel_type ='Human Read').count()


    return render_template('channels.html', Computer = Computer, Captions = Captions, Human = Human, confirmed_channels = cviewsCount, total_views = total_views, channels=channels.items, cols=['Link to Channel', 'Classification','Channel Name', 'Video', 'Title' ,'Views?'], page = page, next_url=next_url, prev_url=prev_url, last_page=last_page, count = C)

@app.route('/notchannels', methods=['GET', 'POST'])
def notchannels():
    page = request.args.get('page', 1, type=int)
    # channels = Channel.query.order_by(Channel.id.asc()).paginate(page, 10, False)
    channels = Channel.query.filter_by(confirm = 1).paginate(page, 10, False)
    C = Channel.query.filter_by(confirm = 1).count()
    last_page = math.ceil(int(C) / int(10))
    print(last_page)
    cviewsCount = Channel.query.filter_by(confirm = 1).count()
    cviews = Channel.query.filter_by(confirm = 1).all()
    views = []
    for c in cviews:
      views.append(c.views)
    # print(channels.videos)
    # print(videos)
    total_views = sum(views)
    page_url = "url_for('allresults', page="
    next_url = url_for('notchannels', page=channels.next_num) \
      if channels.has_next else None
    prev_url = url_for('notchannels', page=channels.prev_num) \
      if channels.has_prev else None



    return render_template('channels.html', confirmed_channels = cviewsCount, total_views = total_views, channels=channels.items, cols=['Link to Channel', 'Classification','Channel Id', 'Video', 'Name', 'Video', 'Name' ,'Confirmed?'], page = page, next_url=next_url, prev_url=prev_url, last_page=last_page, count = C)

@app.route('/allresults', methods=['GET', 'POST'])
def allresults():
    page = request.args.get('page', 1, type=int)
    channels = Channel.query.filter_by(confirm = '0').order_by(Channel.views.desc()).paginate(page, 5, False)
    C = Channel.query.filter_by(confirm = '0').count()
    last_page = math.ceil(int(C) / int(5))
    cviews = Channel.query.filter_by(confirm = 0).all()
    cviewsCount = Channel.query.filter_by(confirm = 0).count()
    views = []
    for c in cviews:
      views.append(c.views)
    Tcviews = sum(views)
    page_url = "url_for('allresults', page="
    next_url = url_for('allresults', page=channels.next_num) \
      if channels.has_next else None
    prev_url = url_for('allresults', page=channels.prev_num) \
      if channels.has_prev else None
    
    return render_template('analyze.html', cviews = Tcviews, channels=channels.items, next_url=next_url, prev_url=prev_url, cols=['Option', 'Video ', 'Video Name', 'Video ', 'Video Name', 'Channel Name', 'Channel Views', 'Link to Channel' , 'About Channel'], page=page, last_page = last_page, count = int(C))

@app.route('/human_channel/<channel_Id>')
def human_channel(channel_Id):
    human_channel1(channel_Id)
    
    return render_template('confirm.html', channel_Id = channel_Id, response = ' not text to speech' )


@app.route('/subtitle_channel/<channel_Id>')
def subtitle_channel(channel_Id):
    subtitle_channel1(channel_Id)
     
    return render_template('confirm.html', channel_Id = channel_Id, response = ' not text to speech')


@app.route('/not_channel/<channel_Id>')
def not_channel(channel_Id):
    not_channel1(channel_Id)
    return render_template('confirm.html', channel_Id = channel_Id, response = ' not text to speech' )

@app.route('/null_channel/<channel_Id>')
def null_channel(channel_Id):
    null_channel1(channel_Id)
    return render_template('confirm.html', channel_Id = channel_Id, response = ' to reset the determination')


@app.route('/channel_update/<channel_Id>')
def update_channel(channel_Id):
    confirm_channel(channel_Id)
    return render_template('confirm.html', channel_Id = channel_Id, response = ' text to speech')
    # form2 = UpdateSiteForm()

@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      "./client_secret.json", scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  session['state'] = state
  print(state)
  print(authorization_url)
  return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  token_url='https://www.googleapis.com/oauth2/v3/token'
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = session['state']
  print(state)
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      "./client_secret.json", scopes=['https://www.googleapis.com/auth/youtube.force-ssl'], state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  authorization_response1 = authorization_response.replace('http://', 'https://') 
  print(authorization_response1)
  # authorization_response = request.build_absolute_uri()        

  # print(parse_authorization_response(authorization_response1))
  flow.fetch_token(authorization_response=authorization_response1)
  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)
  client = build('youtube', 'v3', credentials=credentials)

  return redirect(url_for('search_articles'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}



if __name__ == "__main__":
    app.run(ssl_context=('./ssl.crt', './ssl.key'))
