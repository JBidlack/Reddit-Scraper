#imports needed. The .env file will be .gitignored for security
from dotenv.main import load_dotenv;
import praw;
import os;
import pandas as pd
import datetime
import time

load_dotenv()

#putting the connection info into a try/catch block in case of connection error
try:
    Reddit = praw.Reddit(
        client_id = os.environ['client'],
        client_secret = os.environ['secret'],
        password = os.environ['pw'],
        user_agent = os.environ['user'] + " by u/JBiddyB",
        username = "JBiddyB"
    )
except Exception as e:
    print("Error connecting")
    Reddit = None

if Reddit:
    source = Reddit.subreddit('antiwork').top(limit = 10000)
    posts = {}
    keywords = {"bullsht", "meaningless", "aimless", "purposeless", "futile", "senseless work"}

# create a data structure for each post returned
    data = {
        'Title': [],
        'Body': [],
        'Posted': []
        }
    count = 0
#use a nested for loop to check each post title for the keywords
    for post in source:
        count+=1
        print(count)
        for keyword in keywords:
            if (keyword in post.title.lower() or keyword in post.selftext.lower()) and post.id not in posts:
                posts[post.id] = post
                data['Title'].append(post.title)
                data['Body'].append(post.selftext)
                data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
                print(len(posts))
            if len(posts) == 10:
                break     
        if len(posts) == 10:
                break
# since the reddit API only allows 60 calls per minute, we sleep 
        time.sleep(1)
# use pandas to create a dataframe of the information to be used for exporting to a csv
# the csv is created, keeping the index True to make sorting easier
    df = pd.DataFrame(data)
    df.to_csv('results.csv', index = True)

# Since the code will take a long time to run, the print statement is a simple method of letting me know the process is complete.
    print(len(posts))
    print("Done")
else:
    print("Connection problems. Please try again later")

