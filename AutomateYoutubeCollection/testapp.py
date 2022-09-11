from selenium import webdriver
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/c/Telusko/videos")
titles = driver.find_elements_by_id("video-title")
thumbnail = driver.find_elements_by_id("img")

for title in titles:
    print(title('href'))
    title.find_element()


# content = driver.page_source.encode('utf-8').strip()
# soup = bs(content, 'lxml')
# titles = soup.findAll('a',  id='video-title')
# views =  soup.findAll('span', class_= "style-scope ytd-grid-video-renderer" )
# video_urls = soup.findAll('a',  id='video-title')



# def getVideoID(title):
#     url_data = parse.urlparse(title)
#     query = parse.parse_qs(url_data.query)
#     video_id = query["v"][0]
#
#     return video_id


# def getVideoInfo(titles_tag):
#     video_df = pd.DataFrame(columns=['video_id','video_link','video_title','thumbnail','viewCount','likeCount','commentCount'])
#     for title in titles_tag:
#         video_link  = title.get_attribute("href")
#         video_title = title.text
#
#         video_id = getVideoID(title) #get video ID
#
#         thumbnail = driver.get(f"http://img.youtube.com/vi/{video_id}/0.jpg") # get the thumbnail of the video
#
#         url_video = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&part=statistics&key=" + config.API_KEY
#         response = requests.get(url_video).json()
#         viewCount = response['items'][0]['statistics']['viewCount']
#         likeCount = response['items'][0]['statistics']['likeCount']
#         commentCount = response['items'][0]['statistics']['commentCount']
#         video_df.append(['video_id','video_link','video_title','thumbnail','viewCount','likeCount','commentCount'], ignore_index=True)
#         getVideoComments(video_id)
#         putVideo(video_id)

# def getVideoID(title):
#     url_data = parse.urlparse(title)
#     query = parse.parse_qs(url_data.query)
#     video_id = query["v"][0]
#
#     return video_id


# def getVideoInfo(titles_tag):
#     video_df = pd.DataFrame(columns=['video_id','video_link','video_title','thumbnail','viewCount','likeCount','commentCount'])
#     for title in titles_tag:
#         video_link  = title.get_attribute("href")
#         video_title = title.text
#
#         video_id = getVideoID(title) #get video ID
#
#         thumbnail = driver.get(f"http://img.youtube.com/vi/{video_id}/0.jpg") # get the thumbnail of the video
#
#         url_video = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&part=statistics&key=" + config.API_KEY
#         response = requests.get(url_video).json()
#         viewCount = response['items'][0]['statistics']['viewCount']
#         likeCount = response['items'][0]['statistics']['likeCount']
#         commentCount = response['items'][0]['statistics']['commentCount']
#         video_df.append(['video_id','video_link','video_title','thumbnail','viewCount','likeCount','commentCount'], ignore_index=True)
#         getVideoComments(video_id)
#         putVideo(video_id)