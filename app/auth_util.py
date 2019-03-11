# import google_auth_oauthlib.flow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask import render_template, flash, redirect, url_for, session, request
import googleapiclient.discovery
from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.auth.transport.requests
from oauth2client.client import flow_from_clientsecrets
from google.oauth2 import service_account
# def main():
# 	flow = flow_from_clientsecrets('path_to_directory/client_secrets.json',
# 		                           scope='https://www.googleapis.com/auth/calendar',
# 		                           redirect_uri='http://example.com/auth_return')

def build_client():
	SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
	SERVICE_ACCOUNT_FILE = './youtube-tool-219213-e7f710d3e88a.json'
	credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	client = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
	return client 

# def get_authenticated_service():
# 	# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# 	# the OAuth 2.0 information for this application, including its client_id and
# 	# client_secret.
# 	CLIENT_SECRETS_FILE = "./client_secret.json"
# 	#C:/Users/emr673/PythonTest/Youtube/YouTool
# 	# This OAuth 2.0 access scope allows for full read/write access to the
# 	# authenticated user's account and requires requests to use an SSL connection.
# 	SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
# 	API_SERVICE_NAME = 'youtube'
# 	API_VERSION = 'v3' 
# 	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# 	credentials = flow.run_from	()
# 	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def google_auth():
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    './client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
	flow.redirect_uri = url_for('process', _external=True)

	authorization_response = request.url
	flow.fetch_token(authorization_response=authorization_response)

	# Store the credentials in the session.
	# ACTION ITEM for developers:
	#     Store user's access and refresh tokens in your data store if
	#     incorporating this code into your real app.
	credentials = flow.credentials
	API_SERVICE_NAME = 'youtube'
	API_VERSION = 'v3' 
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
