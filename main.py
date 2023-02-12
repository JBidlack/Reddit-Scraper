"""Reddit Scraper"""
# imports needed. The .env file will be .gitignored for security
import os
import datetime
import time
import pandas as pd
import praw
from dotenv.main import load_dotenv

load_dotenv()


keywords = open('keywords.csv', 'r').readlines()


# putting the connection info into a try/catch block in case of connection error
try:
    REDDIT = praw.Reddit(
        client_id = os.environ['client'],
        client_secret = os.environ['secret'],
        password = os.environ['pw'],
        user_agent = os.environ['user'] + " by u/JBiddyB",
        username = "JBiddyB"
    )
except ConnectionError() as e:
    print("Error connecting")
    REDDIT = None

if REDDIT:
    source = REDDIT.subreddit('antiwork').new(limit = 10000)
    posts = {}
    

# create a data structure for each post returned
    data = {
        'Title': [],
        'Body': [],
        'Posted': []
        }
    COUNT = 0
# use a nested for loop to check each post title for the keywords
    for post in source:
        COUNT+=1
        print(COUNT)
        for keyword in keywords:
            if (keyword in post.title.lower() or keyword
            in post.selftext.lower()) and post.id not in posts:
                posts[post.id] = post
                data['Title'].append(post.title)
                data['Body'].append(post.selftext)
                data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
            if len(posts) == 1000:
                break
        if len(posts) == 1000:
            break
# since the REDDIT API only allows 60 calls per minute, we sleep
        time.sleep(1)

# use pandas to create a dataframe of the information to be used for exporting to a csv
# the csv is created, keeping the index True to make sorting easier
    df = pd.DataFrame(data)
    df.to_csv('results3.csv', index = True)

# Since the code will take a long time to run,
# the print statement is a simple method of letting me
# know the process is complete.

    print(len(posts))
    print("Done")
else:
    print("Connection problems. Please try again later")