# reddit-scraping

The scripts in this repository are used to scrape data from a collection of Reddit posts and perform sentiment analysis on the comments.

These scripts require two python packages to run: [NLTK](https://www.nltk.org/install.html) and [PRAW](https://praw.readthedocs.io/en/stable/getting_started/installation.html)\
The sentiment analysis script also assumes you have these NLTK libraries installed:

If you are on the Beartooth cluster you do not need to worry about installing any of these.\
To run these scripts, navigate to the ``reddit-scraping/scripts`` directory and run this command
```
sbatch bashReddit.sh
```
This will load all of the required modules and run both scripts back to back.