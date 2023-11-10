## Author: Carver Bray
## 
## Date Created: 11/6/2023
##
## Last Modified: 11/6/2023
##
## Script Purpose: Scrapes a group of reddit posts using the PRAW library and
##   outputs certain data into files to then go through sentiment analysis in a
##   separate script later.

import praw
from datetime import datetime
import os

# get Reddit instance, which gives us access to the Reddit API, in general
# NOTE: Do NOT put quotes ("") around items in the praw.ini file
# This command will fail if you do that
reddit = praw.Reddit("bot1")

print(reddit.read_only)

# create a list of submissions to go through
# later this will be handled through a different file to make 
# adding/removing reddit links easier
url_list = [
    "https://www.reddit.com/r/Superstonk/comments/z3mcze/wen_dfv/",
    "https://www.reddit.com/r/Superstonk/comments/yw9g65/dr_susanne_trimbath_on_twitter/"
]

# Needs from Madi:
# Top 100 Comments: This includes the replies on each initial comment, so get
#   100 comments total, in general.
# 
# Users: What user posted what? That includes user who posted the initial post
#   and users who post comments. Likely it should look like...
#   user123: <content of comment>
#
# Original Post Content: Full text of original post. Indicate if the post
#   was a photo, video, or tweet. 
#
# Post date and time: get the date and time the original post was made

# file writing goes like so:
# file = open("filename", "w")
# "w" creates a file if it doesn't exist and will overwrite it if it does

for url in url_list:
    submission = reddit.submission(url=url)
    print(submission)
    # replace_more gets rid of the "load more comments" thing that pops up on 
    # Reddit so that all comments are loaded into the comments field
    submission.comments.replace_more(limit=None)
    submission.comment_sort = "top"

    subFile = open("../api-results/"+submission.title+".md", "w")

    commentList = submission.comments.list()

    for i in range(0,99):
        timePosted = datetime.fromtimestamp(commentList[i].created_utc)
        timePosted = timePosted.strftime("%m/%d/%Y, %H:%M:%S")

        username = "[deleted user]" if commentList[i].author == None else (
            commentList[i].author.name) 

        content = username + " commented at " + (
            timePosted + ": " + commentList[i].body)
        
        subFile.write("\n"+content+"\n")
    
    subFile.close()