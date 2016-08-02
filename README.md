# twitass
Scrapes tweets from the Twitter Advanced Search webpage - bypasses the 10 day limit of the public API

# How do I get set up? #

## Clone the repo

```
git clone https://github.com/gutfeeling/twitass.git
cd twitass
```


## Install dependencies

### First the Python packages

1. Create a virtualenv
  - If you want to use python 2

    ```  
    virtualenv venv
    ```
  - If you want to use python 3

    ```
    virtualenv -p python3 venv
    ```

2. Activate the virtualenv

  ```
  source venv/bin/activate
  ```

3. Install the python modules

  - If you want to use python 2

    ```  
    pip install -r requirements2.txt
    ```
  - If you want to use python 3

    ```
    pip install -r requirements3.txt
    ```

### Then the non Python dependencies

4. Download Chromedriver from [this link](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Define Environment Variables

You need to define a environment variable CHROMEDRIVER_PATH and point it to the location of the chromedriver executable. On UNIX based systems, use the following command.

```
export CHROMEDRIVER_PATH = "/path/to/chromedriver"
```

## Start scraping

Here is a basic example which searches for the word "python" in the Twitter Advance Search webpage. We simulate scrolling the page 20 times.  

  ```python
  >>> from scraper import AdvancedSearchScraper
  >>> ass = AdvancedSearchScraper("python", 20)
  >>> tweets = ass.scrape()    # Scrolls 20 times and returns all the loaded tweets as a list
  >>> tweets[0]    # Each list element is a dict containing data of one tweet
  {'tweet_permalink': u'/tonyojeda3/status/760282753795522560', 
   'tweet_text': '<p class="TweetTextSize js-tweet-text tweet-text" data-aria-label-part="0" lang="en">Getting Started 
                  with Spark (in <strong>Python</strong>) <a class="twitter-timeline-link" data-expanded-url="http://bit.ly/pyspark1" 
                  dir="ltr" href="https://t.co/VMv6NVveUT" el="nofollow" target="_blank" title="http://bit.ly/pyspark1">
                  <span class="tco-ellipsis"></span><span class="invisible">http://</span><span class="js-display-url">
                  bit.ly/pyspark1</span><span class="invisible"></span><span class="tco-ellipsis"><span class="invisible">
                  </span></span></a> <a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" 
                  dir="ltr" href="/hashtag/DataScience?src=hash"><s>#</s><b>DataScience</b></a> <a class="twitter-hashtag 
                  pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" href="/hashtag/BigData?src=hash"><s>#</s>
                  <b>BigData</b></a> <a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" 
                  href="/hashtag/Hadoop?src=hash"><s>#</s><b>Hadoop</b></a> <a class="twitter-hashtag pretty-link js-nav" 
                  data-query-source="hashtag_click" dir="ltr" href="/hashtag/ApacheSpark?src=hash"><s>#</s><b>ApacheSpark</b></a> 
                  <a class="twitter-hashtag pretty-link js-nav" data-query-source="hashtag_click" dir="ltr" 
                  href="/hashtag/Python?src=hash"><s>#</s><b><strong>Python</strong></b></a></p>', 
    'author_name': u'Tony Ojeda', 
    'tweet_time': u'6:15 PM - 1 Aug 2016', 
    'tweet_timestamp': u'1470100508000', 
    'favorites': 0, 
    'author_href': u'/tonyojeda3', 
    'tweet_id': u'760282753795522560', 
    'author_handle': u'tonyojeda3', 
    'retweets': 0, 
    'author_id': u'45048508'}
  ```


