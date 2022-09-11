#Google API:
import pymongo
API_KEY ='AIzaSyBBhhYEe9OHECZ1xzL0WXkJE2ROx224DGA'

#Snowflake cerdentials:

snow_username = 'abdulrahuman1631'
snow_password='#@Charecters7'
snow_account='OAb35976.us-east-1'
snow_wharehouse='COMPUTE_WH'
snow_database='YOUTUBEDATA'
snow_password_alchemy = '#%40Charecters7'


#AWS credentials:
aws_awsIAMuser = "youtubeuser"
aws_ACCESS_KEY = "AKIA34S5HAFFXOQVC2PL"
aws_SECRET_ACCESS_KEY = "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"
BUCKET_NAME = "youtubeideoest"
aws_region ="US East (N. Virginia) us-east-1"

#MongoDB credentials:
client = pymongo.MongoClient("mongodb+srv://abdulrah77:mongodb@cluster0.eveyiyi.mongodb.net/?retryWrites=true&w=majority")
db = client['Youtube']