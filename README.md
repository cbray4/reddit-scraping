# reddit-scraping

The scripts in this repository are used to scrape data from a collection of Reddit posts and perform sentiment analysis on the comments.

These scripts require two python packages to run: [NLTK](https://www.nltk.org/install.html) and [PRAW](https://praw.readthedocs.io/en/stable/getting_started/installation.html)\
The sentiment analysis script also assumes you have these NLTK libraries installed: ``SentimentIntensityAnalyzer, word_tokenize, stopwords, and WordNetLemmatizer``\
If you are on the Beartooth cluster you do not need to worry about installing any of these.

To run these scripts, navigate to the ``projects/reddit-scraping/scripts`` directory and run this command
```
sbatch bashReddit.sh
```
This will load all of the required modules and run both scripts back to back. Output for the sentiment analysis can be found in the ``reddit-scraping/sentiment-results`` directory, with results for each post in their own file. Output for the scraping script can be found in ``reddit-scraping/api-results`` if you wish to look at those.

