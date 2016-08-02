import time
import json
import warnings

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

warnings.filterwarnings('ignore')

class AdvancedSearchScraper(object):

    def __init__(self, all_of_these_words, limit = 100):
        self.all_of_these_words = all_of_these_words
        self.driver = webdriver.PhantomJS()
        if limit:
            self.limit = limit
        else:
            self.limit = float("inf")

    def first_page_url(self):
        query_dict = {"src" : "typd",
                      "q" : self.all_of_these_words,
                      "f" : "tweets",
                      }
        query_string = urlencode(query_dict)
        url = "https://twitter.com/search?" + query_string
        return url

    def ajax_call_url(self, oldest_tweet_id, newest_tweet_id):
        query_dict = {"src" : "typd",
                      "q" : self.all_of_these_words,
                      "f" : "tweets",
                      "vertical" : "default",
                      "include_available_features" : 1,
                      "include_entities" : 1,
                      "reset_error_state" : "false",
                      "max_position" : "TWEET-%s-%s" %(oldest_tweet_id, newest_tweet_id),
                      }
        query_string = urlencode(query_dict)
        url = "https://twitter.com/i/search/timeline?" + query_string
        return url

    def scrape(self):
        self.tweets = []

        #first-page
        self.driver.get(self.first_page_url())
        self.tweets+=self.get_tweets_from_html(self.driver.page_source)
        self.driver.close()

        #ajax
        if len(self.tweets)>0:

            newest_tweet_id = self.tweets[0]['tweet_id']
            oldest_tweet_id = self.tweets[-1]['tweet_id']
            has_more_items = True

            while len(self.tweets) < self.limit and has_more_items:

                time.sleep(1)

                response = requests.get(self.ajax_call_url(oldest_tweet_id, newest_tweet_id),
                                        verify = False)
                json_data = json.loads(response.text)
                self.tweets+=self.get_tweets_from_html(json_data["items_html"])
                oldest_tweet_id = self.tweets[-1]['tweet_id']
                has_more_items = json_data["has_more_items"]

        return self.tweets





    def get_tweets_from_html(self, html_doc):
        tweetlist = []
        html_soup = BeautifulSoup(html_doc, "html.parser")
        tweet_soup_list = html_soup.find_all("div", {"class" : "original-tweet"})
        for tweet_soup in tweet_soup_list:
            tweet_dict = {
                "tweet_id" : tweet_soup["data-tweet-id"],
                "author_name" : tweet_soup["data-name"],
                "author_handle" : tweet_soup["data-screen-name"],
                "author_id" : tweet_soup["data-user-id"],
                "author_href" : tweet_soup.find("a",{"class" : "account-group"})["href"],
                "tweet_permalink" : tweet_soup["data-permalink-path"],
                "tweet_text" : str(tweet_soup.find("p", {"class" : "tweet-text"})),
                "tweet_time" : tweet_soup.find("a",{"class" : "tweet-timestamp"})["title"],
                "tweet_timestamp" : tweet_soup.find(
                    "span",{"class" : "_timestamp"})["data-time-ms"],
                "retweets" : int(tweet_soup.find(
                    "span",{"class" : "ProfileTweet-action--retweet"}).find(
                    "span", {"class" : "ProfileTweet-actionCount"})['data-tweet-stat-count']),
                "favorites" : int(tweet_soup.find(
                    "span",{"class" : "ProfileTweet-action--favorite"}).find(
                    "span", {"class" : "ProfileTweet-actionCount"})['data-tweet-stat-count']),
                }
            tweetlist.append(tweet_dict)
        return tweetlist
