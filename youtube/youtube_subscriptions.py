#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

from oauth2client.file import Storage
import datetime
import sys
from sendgrid import *

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets_1.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user"s account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
								   CLIENT_SECRETS_FILE))


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = "https://www.googleapis.com/auth/youtube"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "Gmail API Python Quickstart"

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser("~")
	credential_dir = os.path.join(home_dir, ".credentials")
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   "youtube-python-quickstart.json")
	print credential_path
	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		# if flags:
		credentials = tools.run_flow(flow, store)
		# else: # Needed only for compatibility with Python 2.6
			# credentials = tools.run(flow, store)
		print("Storing credentials to " + credential_path)
	return credentials

# This method calls the API"s youtube.subscriptions.insert method to add a
# subscription to the specified channel.
def get_subscription(youtube):
	# print(youtube)
	subscription_response = youtube.subscriptions().list(part="snippet",
	mine=True,maxResults = 50).execute()
	#for i in add_subscription_response:
	# print i
	return subscription_response

def get_videos(youtube, channelId):
	video_response = youtube.search().list(part="snippet", channelId = channelId, maxResults = 50, order = "rating").execute()
	return video_response

def main():
	subscriptions = {}
	videos = {}
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build("youtube", "v3", http=http)
	for i in get_subscription(service)["items"]:
		subscriptions[i["snippet"]["title"]]= i["snippet"]["resourceId"]["channelId"]
	print subscriptions
	for i in subscriptions.keys():
		print get_videos(service, subscriptions[i])
		videos[i] = get_videos(service,subscriptions[i])
	print videos

if __name__ == "__main__":
	main()


# if __name__ == "__main__":
#   argparser.add_argument("--channel-id", help="ID of the channel to subscribe to.",
#     default="UCtVd0c0tGXuTSbU5d8cSBUg")
#   args = argparser.parse_args()

#   youtube = get_authenticated_service(args)
#   try:
#     channel_title = add_subscription()
#     print channel_title
#   except HttpError, e:
#     print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
#   else:
#     print "A subscription to "%s" was added." % channel_title