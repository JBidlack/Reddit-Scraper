"""SubReddit Searcher created by John Bidlack"""

# imports needed. The .env file will be .gitignored for security
import os
import datetime
import pandas as pd
import praw
import time
from builtins import any
from dotenv.main import load_dotenv

load_dotenv()

# Open and read in each file. Each file represents the column
# whos name coresponds with the file name
# flunkies = open('flunkies.csv', 'r').readlines()
# boxTicker = open('boxticker.csv', 'r').readlines()
# ductTaper = open('ducttaper.csv', 'r').readlines()
# goons = open('goon.csv', 'r').readlines()
# taskMaster = open('taskmaster.csv', 'r').readlines()

keywords = open('keywords.csv', 'r').readlines()

# flunkyCount = 0
# boxCount = 0
# ductCount = 0
# goonCount = 0
# taskCount = 0

# putting the connection info into a try/catch block in case of connection error.
# variable names are contained in a .env file to provide privacy
try:
    REDDIT = praw.Reddit(
        client_id = os.environ['client'],
        client_secret = os.environ['secret'],
        password = os.environ['pw'],
        user_agent = os.environ['user'] + " by u/JBiddyB",
        username = "JBiddyB"
    )
except Exception() as e:
    print("Error connecting")
    REDDIT = None

remaining_requests = REDDIT.auth.limits.get("remaining")

if REDDIT:
    source = REDDIT.subreddit('antiwork').new(limit = 1000)
    posts = {}   


# create a data structure for each post returned
    data = {
        'Title': [],
        'Body': [],
        'Posted': [],
        'Shortlink': []
        }
    COUNT = 0
# use a nested for loop to check each post title for the keywords
# or phrases contained in each file
    for post in source:
        COUNT+=1
        print(COUNT)

        remaining_requests = REDDIT.auth.limits.get("remaining")
        reset_timestamp = REDDIT.auth.limits.get("reset_timestamp")

        # Check if rate limit has been exceeded
        if remaining_requests == 0:
            # Wait for rate limit to expire
            REDDIT.auth.limits.update()
            wait_time = reset_timestamp - time.time()
            print(f'waiting {wait_time}')
            time.sleep(wait_time)
        data['Title'].append(post.title)
        data['Body'].append(post.selftext)
        data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        data['Shortlink'].append(post.shortlink)
        # for keyword in keywords:
        #     if (keyword in post.title.lower() or keyword
        #     in post.selftext.lower()) and post.id not in posts:

        #         posts[post.id] = post
        #         data['Title'].append(post.title)
        #         data['Body'].append(post.selftext)
        #         data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        #         data['Shortlink'].append(post.shortlink)
        # for box in boxTicker:
        #     if (box in post.title.lower() or box
        #     in post.selftext.lower()) and post.id not in posts:
        #         boxCount += 1
        #         posts[post.id] = post
        #         data['Title'].append(post.title)
        #         data['Body'].append(post.selftext)
        #         data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        #         data['Shortlink'].append(post.shortlink)
        # for duct in ductTaper:
        #     if (duct in post.title.lower() or duct
        #     in post.selftext.lower()) and post.id not in posts:
        #         ductCount += 1
        #         posts[post.id] = post
        #         data['Title'].append(post.title)
        #         data['Body'].append(post.selftext)
        #         data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        #         data['Shortlink'].append(post.shortlink)
        # for goon in goons:
        #     if (goon in post.title.lower() or goon
        #     in post.selftext.lower()) and post.id not in posts:
        #         goonCount += 1
        #         posts[post.id] = post
        #         data['Title'].append(post.title)
        #         data['Body'].append(post.selftext)
        #         data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        #         data['Shortlink'].append(post.shortlink)    
        # for task in taskMaster:
        #     if (task in post.title.lower() or task
        #     in post.selftext.lower()) and post.id not in posts:
        #         taskCount += 1
        #         posts[post.id] = post
        #         data['Title'].append(post.title)
        #         data['Body'].append(post.selftext)
        #         data['Posted'].append(datetime.datetime.fromtimestamp(post.created_utc))
        #         data['Shortlink'].append(post.shortlink)    

# use pandas to create a dataframe of the information to be used for exporting to a csv
# the csv is created, keeping the index True to make sorting easier
    df = pd.DataFrame(data)
    df.to_csv('results3-4-23.csv', index = True)




# Since the code will take a long time to run,
# the print statement is a simple method of letting me
# know the process is complete.

    print(len(posts))
    print("Done")

# In the event a connection with Reddit fails, an error message is displayed
else:
    print("Connection problems. Please try again later")