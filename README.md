# twitass
Scrapes tweets from the Twitter Advanced Search webpage - bypasses the 7 day historical limit of the public API

# Installation 

 ```
 pip install -e git+https://github.com/gutfeeling/twitass#egg=twitass
 ```
  
# How to scrape

twitass exposes a super simple API for scraping tweets. Here is a basic example which searches for the word "python" in the Twitter Advance Search webpage and returns the first 200 tweets.  

  ```python
  >>> from scraper import AdvancedSearchScraper
  >>> ass = AdvancedSearchScraper("python", 200)
  >>> tweets = ass.scrape()    # Returns the first 200 tweets in a list
  >>> tweets[0]    # Each list element is a dict containing data of one tweet
  {'tweet_timestamp': '1470408709000', 
   'tweet_id': 761575443145162752, 
   'author_href': '/ulysseas', 
   'tweet_permalink': '/ulysseas/status/761575443145162752', 
   'retweets': 0, 
   'author_name': 'Don Sheu 許家豪', 
   'tweet_time': '7:51 AM - 5 Aug 2016', 
   'author_handle': 'ulysseas', 
   'tweet_language': 'en', 
   'favorites': 0, 
   'author_id': 229946505, 
   'tweet_text': "@DaveParkerSEA @DRNilssen in Rio? Hope you connect w/ @ChicagoPython 's @brianray , Brian's my best friend, introduced me to Python community"
   }
  ```


