#!/usr/bin/python
'''Uploads a video to YouTube.'''

from http import client
import httplib2
import os
import random
import time
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, client.NotConnected,
                        client.IncompleteRead, client.ImproperConnectionState,
                        client.CannotSendRequest, client.CannotSendHeader,
                        client.ResponseNotReady, client.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = ''

#SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/upload/youtube/v3/thumbnails/set', 'https://www.googleapis.com/auth/youtube.force-ssl']
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


# Authorize the request and store authorization credentials.
def get_authenticated_service(credentialsPath=""):
    CLIENT_SECRETS_FILE=f'{credentialsPath}/client_secret.json'
    if os.path.exists(f'{credentialsPath}/credentials.json'):
        with open(f'{credentialsPath}/credentials.json') as json_file:
            data = json.load(json_file)
            credentials = google.oauth2.credentials.Credentials(
                token=data['token'],
                refresh_token=data['refresh_token'],
                token_uri=data['token_uri'],
                client_id=data['client_id'],
                client_secret=data['client_secret'],
                scopes=data['scopes']
            )
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(success_message="Heyy, yippie, you're authenticated ! You can close this window now !", authorization_prompt_message="Please authorize this app to upload videos on your YouTube account !")
        with open(f'{credentialsPath}/credentials.json', 'w') as outfile:
            outfile.write(credentials.to_json())
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def initialize_upload(youtube, options):
    tags = None
    if options['keywords']:
        tags = options['keywords'].split(',')

    body = dict(
        snippet=dict(
            title=options['title'],
            description=options['description'],
            tags=tags,
            categoryId=options['category'],
            defaultLanguage='en'
        ),
        status=dict(
            privacyStatus=options['privacyStatus'],
            selfDeclaredMadeForKids=False
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True)
    )

    videoid = resumable_upload(insert_request)
    return videoid


def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print('Video id "%s" was successfully uploaded.' %
                          response['id'])
                    return response['id']
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)

def upload_video(path, title, description, category, keywords, privacyStatus='private', credentials_path=""):
    options = {
        'file': path +"/montage.mp4",
        'title': title,
        'description': description,
        'category': category,
        'keywords': keywords,
        'privacyStatus': privacyStatus
    }
    youtube = get_authenticated_service(credentials_path)
    try:
        videoid = initialize_upload(youtube, options)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    upload_thumbnail(videoid, path + "/miniature.png", credentials_path)

def upload_thumbnail(video_id, file, credentials_path=""):
    youtube = get_authenticated_service(credentials_path)
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=file
    ).execute()