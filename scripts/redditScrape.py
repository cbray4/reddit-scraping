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

firstSubmission = reddit.submission(url=url_list[0])
print(firstSubmission)

firstSubmission.comments.replace_more(limit=None)
firstSubmission.comment_sort = "top"
for top_level_comment in firstSubmission.comments:
    print(top_level_comment.body)