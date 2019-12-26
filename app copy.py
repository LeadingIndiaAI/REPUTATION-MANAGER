from flask import Flask,render_template,redirect,request
import os
import sys
import google.oauth2.credentials
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
import tweepy as tw
import requests
import json



#for youtube
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()
 
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
 
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            commentinfo=[]
            info1 = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            info2 = item['snippet']['topLevelComment']['snippet']['publishedAt']
            info3 = item['snippet']['topLevelComment']['snippet']['likeCount']
            info4 = item['snippet']['topLevelComment']['snippet']['viewerRating']
            info5 = item['snippet']['totalReplyCount']
            info6 = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            commentinfo.append(info1)
            commentinfo.append(info2)
            commentinfo.append(info3)
            commentinfo.append(info4)
            commentinfo.append(info5)
            commentinfo.append(info6)
            commentinfo.append(comment)
            comments.append(commentinfo)

        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments

def get_videos(service, **kwargs):
    final_results = []
    results = service.search().list(**kwargs).execute()
    i = 0
    max_pages = 1
    while results and i < max_pages:
        final_results.extend(results['items'])

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break

    return final_results

def search_videos_by_keyword(service, **kwargs):
    
    results = get_videos(service, **kwargs)
    for item in results:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
        print(comments)
        return comments

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
service = get_authenticated_service()
comments_from_youtube =search_videos_by_keyword(service, q="macbook", part='id,snippet', eventType='completed', type='video')
        
