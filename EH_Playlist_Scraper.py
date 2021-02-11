#START HERE
#https://www.youtube.com/watch?v=th5_9woFJmk
from googleapiclient.discovery import build

api_key = 'AIzaSyBT8wA9JslanCzQeKmqQoZShVVtMXBUApI'
youtube = build('youtube', 'v3', developerKey = api_key)
playlist_id = 'PLhyKYa0YJ_5Aq7g4bil7bnGi0A8gTsawu'  


def get_yt_playlist(token='', playlist = '', num_vids = 50, target = "snippet"):
    return youtube.playlistItems().list(
        part= target,
        playlistId = playlist,
        maxResults = num_vids,
        pageToken = token
        ).execute()


def extract_vid_ids(json_dict={}):
    temp_list = []

    for vid in json_dict["items"]:        
        vid_id = vid['contentDetails']['videoId']
        temp_list.append(vid_id)

    return ','.join(temp_list)


def get_vid_stats(vidIds = ''):
    return youtube.videos().list(
    part="snippet,statistics,contentDetails",
    id= vidIds
    ).execute()


import isodate
def scrape_yt_vids_dict(statDictObj = {}):

    tempList = []

    for i in statDictObj['items']:
        
        vidId = i['id']
        #need contentDetails in scrape_yt_vids_dict
        playtime = i['contentDetails']['duration']  
        #convert PT5M38S in actual seconds
        vidDuration = isodate.parse_duration(playtime).total_seconds()
        vidTitle = i['snippet']['title']
        #[:10] only want upload dates, not hour 
        vidDate = i['snippet']['publishedAt'][:10]              
        vidViews = i['statistics']['viewCount']
        vidLikes = i['statistics']['likeCount']
        vidDislikes = i['statistics']['dislikeCount']
        vidComments = i['statistics']['commentCount']


        tempList.append((vidTitle, vidDate, vidViews,
            vidLikes, vidDislikes, vidComments,vidId,vidDuration))

    return tempList


keep_running = True
next_token = ''
youtube_json_list = []
while keep_running == True:

    raw_json = get_yt_playlist(next_token, playlist_id, 50, "contentDetails")
    next_token = raw_json.get('nextPageToken', '')
    youtube_json_list.append(raw_json)

    if next_token == '':
        keep_running = False


all_vid_stats = []
for i in youtube_json_list:
    vid_ids = extract_vid_ids(i)
    vid_stats = get_vid_stats(vid_ids)
    all_vid_stats.append(vid_stats)


final_playlist_stats = []
for i in all_vid_stats:
    x = scrape_yt_vids_dict(i)
    final_playlist_stats.extend(x)


import os
path = os.getenv("USERPROFILE") + '\\Documents\\GitHub\\EH-Youtube\\'


from datetime import date
today = str(date.today())
csvName = 'EH Playlist'+ ' ' + today +".csv"


import csv
with open(path+csvName, 'w', newline='',encoding='UTF-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for currentRow in final_playlist_stats:
        csvwriter.writerow(currentRow)
