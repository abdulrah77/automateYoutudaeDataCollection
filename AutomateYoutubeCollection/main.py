from flask import Flask, render_template, request
import requests
import urllib.parse as parse
from googleapiclient.discovery import build
import pandas as pd
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
import time
import snowflake.connector as sf
import base64
from sqlalchemy import create_engine
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# channel_url= "https://www.youtube.com/c/sudhanshukumarall"

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET'])
def getChannelInfo():
    try:
        searchString = request.form['content'].replace(" ", "")
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
        driver.get(searchString)
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'video-title'))
            WebDriverWait(driver, timeout).until(element_present)
            channel_finder = driver.find_element(By.ID, "video-title")
            channel= getVideoID(channel_finder.get_attribute("href"))
        except TimeoutException:
            print ("Loading took too much time!")
    except:
        pass
    video_df = pd.DataFrame(columns=['video_id', 'video_link', 'video_title',  'viewCount', 'likeCount', 'commentCount'])
    channel_name, channel_id = getChannelName(channel)
    channel_name = "_".join(channel_name.split())
    video_df = getVideos(video_df, channel_id, channel_name)
    cur = connectSF(channel_name)
    new_video_df = update_db(cur, video_df, channel_name)
    new_video_df.head()
    append_from_df_to_db(new_video_df,cur, channel_name)

    return "Succesfully Loaded"


def getChannelName(channel_id):
    url = "https://www.googleapis.com/youtube/v3/videos?id="+channel_id+"&part=snippet&key="+config.API_KEY
    response = requests.get(url).json()
    channel_name = response['items'][0]['snippet']['channelTitle']
    channel_id = response['items'][0]['snippet']['channelId']

    return channel_name, channel_id

def getVideoID(channel):
    url_data = parse.urlparse(channel)
    query = parse.parse_qs(url_data.query)
    video_id = query["v"][0]

    return video_id


def getVideos(df, channel_id, channel_name):
    pageToken = ""
    url = "https://www.googleapis.com/youtube/v3/search?key=" + config.API_KEY + "&channelId=" + channel_id + "&part=snippet,id&order=date&maxResults=1000" + pageToken
    response = requests.get(url).json()
    time.sleep(1)
    count=1
    comment_df = pd.DataFrame(columns=['video_id', 'commentorname', 'comments'])  # upload in mongo DB
    for video in response['items']:
        if video['id']['kind'] == "youtube#video" and count<51:
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail = base64.b64encode(requests.get(f"http://img.youtube.com/vi/{video}/0.jpg").content)

            view_count,like_count,comment_count = getVideoDetails(video_id)
            getVideoComments(video_id, comment_df, thumbnail, channel_name)

            # save data in pandas df
            df = df.append(
                {'video_id': video_id, 'video_title': video_title,'video_link': video_link,  'view_count': view_count,
                 'like_count': like_count, 'comment_count': comment_count}, ignore_index=True)

            putVideo(video_id, channel_name)

            count += 1

    return df


def getVideoDetails(video_id):
    url_video = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&part=statistics&key=" + config.API_KEY
    response = requests.get(url_video).json()
    view_count = response['items'][0]['statistics']['viewCount']
    like_count = response['items'][0]['statistics']['likeCount']
    comment_count = response['items'][0]['statistics']['commentCount']

    return view_count, like_count, comment_count


def getVideoComments(video_id, comment_df, thumbnail, channel_name):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    try:
        video_response = youtube.commentThreads().list(part='snippet, replies', videoId=video_id).execute()

        for video in video_response['items']:
            commentor_name = video['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments = video['snippet']['topLevelComment']['snippet']['textOriginal']
            tmp_dict = {'video_id': video_id, 'commentorname': commentor_name, 'comments': comments}
            comment_df = comment_df.append(tmp_dict, ignore_index=True)
    except:
        pass

    updatecomments(comment_df, thumbnail, channel_name, video_id)


# CONNECT TO SNOWFLAKE DATABASE AND DUMP THE DATA
def connectSF(channel_name):
    conn = sf.connect(user=config.snow_username, password=config.snow_password, account=config.snow_account, wharehouse=config.snow_wharehouse)
    cur = conn.cursor()
    query = "Use Database youtubeData"
    cur.execute(query)
    create_table(cur, channel_name)

    return cur



def create_table(curr, channel_name):
    query = (f'''CREATE TABLE IF NOT EXISTS {channel_name} (

            video_id VARCHAR(255) PRIMARY KEY,
            video_link VARCHAR(255),
            video_title TEXT NOT NULL,
            view_count INTEGER NOT NULL,
            like_count	INTEGER NOT NULL,
            comment_count INTEGER NOT NULL)

            ''')
    curr.execute(query)

def update_db(curr,df, channel_name):
    tmp_df = pd.DataFrame(columns=['video_id', 'video_link', 'video_title', 'viewCount', 'likeCount', 'commentCount'])
    for i,row in df.iterrows():
      if check_if_video_exists(curr,row['video_id'], channel_name):
          pass
      else:
          tmp_df = tmp_df.append(row)
          pass
    return tmp_df


def check_if_video_exists(curr, video_id, channel_name):
    query = (f""" select * from  {channel_name}  where video_id = ?;""")

    data_to_check = (video_id,)
    curr.execute(query, data_to_check)

    return curr.fetchone() is not None


def append_from_df_to_db(df, curr, channel_name):
    conn_string = f"snowflake://{config.snow_username}:{config.snow_password_alchemy}@{config.snow_account}/{config.snow_database}/{config.snow_schema}?warehouse={config.snow_wharehouse}"
    engine = create_engine(conn_string)
    connection = engine.connect()
    if_exists = 'replace'


    with connection as con:
        df.to_sql(name=channel_name.lower(), con=con, if_exists=if_exists, index=False)


def putVideo(video_id, channel_name):
    s3 = boto3.resource('s3', aws_access_key_id=config.aws_ACCESS_KEY, aws_secret_access_key=config.aws_SECRET_ACCESS_KEY)
    link = f"https://www.youtube.com/watch?v={video_id}"

    with requests.get(link, stream=True) as r:
        s3.Bucket(config.BUCKET_NAME).put_object(Body=r.content, Key=channel_name + '/' + video_id)


def updatecomments(comment_df,thumbnail, channel_name, video_id):

    collection = config.db[channel_name]
    comment_dict = comment_df.to_dict("records")
    for comment in comment_dict:
        collection.insert_one(comment)
    collection.insert_one({"video_id": video_id,"thumbnail": thumbnail})


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
    # getChannelInfo(channel_url)


