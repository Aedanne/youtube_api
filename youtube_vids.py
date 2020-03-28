# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# pip install --upgrade google-api-python-client
# pip install --upgrade google-auth-oauthlib google-auth-httplib2
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from pytube import YouTube

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "SECRETS.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    video_id_list = []
    get_videos(youtube, video_id_list, None)
    print(video_id_list)
    download_videos(video_id_list)


def download_videos(video_id_list):
    f = open("video_ids.txt", "r")
    downloaded_ids = set()
    for line in f.readlines():
        downloaded_ids.add(line.rstrip())
    f.close()
    for video_id in video_id_list:
        if video_id not in downloaded_ids:
            try:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                youtube = YouTube(video_url)
                video = youtube.streams.first()
                video.download("dir")
                f = open("video_ids.txt", "a")
                f.writelines(f"{video_id}\n")
                f.close()
            except:
                break


def get_videos(youtube, video_id_list, page_token):
    if page_token is None:
        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = "id",
            maxResults = 2
        )
    else:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId="id",
            maxResults=2,
            pageToken=page_token

        )
    response = request.execute()

    video_items = response['items']
    for video_item in video_items:
        video_id = video_item['snippet']['resourceId']['videoId']
        # print(f"video_id = {video_id}")
        video_id_list.append(video_id)

    try:
        next_page_token = response['nextPageToken']
    except KeyError:
        next_page_token = None

    next_page_token = None
    if next_page_token is not None:
        get_videos(youtube, video_id_list, next_page_token)


if __name__ == "__main__":
    main()