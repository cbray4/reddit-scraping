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

    subFile = open("../api-results/"+submission.title+".md", "w")

    # === INITIAL POST SECTION ===
    author = "[deleted user]" if submission.author == None else (
            submission.author.name)
    flair = submission.link_flair_text
    title = submission.title
    body = submission.selftext
    embed = submission.url
    originalTimePosted = datetime.fromtimestamp(submission.created_utc)
    originalTimePosted = originalTimePosted.strftime("%m/%d/%Y, %H:%M:%S")

    fullContent = (author + " posted " + title + " at " + originalTimePosted)
    if embed != submission.permalink:
        fullContent += "\n with link " + embed
    if flair != None:
        fullContent += "\n with flair " + flair
    
    subFile.write(fullContent+"\n")

    # Delimiter for the sentiment analaysis script, since the initial post
    # is not a part of the analysis
    subFile.write("\nCOMMENTS-BEGIN:")

    # === COMMENTS SECTION ===

    # when going through replies, put "replied to" instead of "commented"
    # for the sentiment analysis stuff

    # replace_more gets rid of the "load more comments" thing that pops up on 
    # Reddit so that all comments are loaded into the comments field
    submission.comments.replace_more(limit=None)
    submission.comment_sort = "top"

    # this is for a depth first search algorithm
    commentQueue = submission.comments[:]

    for i in range(0,99):
        comment = commentQueue.pop(0)

        username = "[deleted user]" if comment.author == None else (
            comment.author.name) 
        # skip automod comments
        if username == "Superstonk_QV":
            continue
        timePosted = datetime.fromtimestamp(comment.created_utc)
        timePosted = timePosted.strftime("%m/%d/%Y, %H:%M:%S")

        # Determine if comment is a reply or not
        # reddit.comment(parent_id) will get the parent comment to do stuff with
        # string[:2] is first two letters
        if comment.parent_id[:2] != "t3":
            content = username + " replied to " + previousUser
        else:
            content = username + " commented"

        content += " at " + timePosted + ": " + comment.body

        subFile.write("\n"+content+"\n")

        previousUser = username

        commentQueue[0:0] = comment.replies
    
    subFile.close()
