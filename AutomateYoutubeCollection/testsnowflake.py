import snowflake.connector as sf


snow_username = 'abdulrahuman1631'
snow_password='#@Charecters7'
snow_account='OAb35976.us-east-1'
snow_wharehouse='COMPUTE_WH'
snow_database='YOUTUBEDATA'

conn = sf.connect(user=snow_username, password=snow_password,account= snow_account, wharehouse=snow_wharehouse)
