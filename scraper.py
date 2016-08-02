import time
import os

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from bs4 import BeautifulSoup
from selenium import webdriver


class AdvancedSearchScraper(object):

    def __init__(self, all_of_these_words, scroll_limit = 10):
        self.all_of_these_words = all_of_these_words
        self.driver = webdriver.Chrome(os.environ["CHROMEDRIVER_PATH"])
        if scroll_limit:
            self.scroll_limit = scroll_limit
        else:
            self.scroll_limit = float("inf")

    def first_page_url(self):
        query_dict = {"src" : "typd",
                      "q" : self.all_of_these_words,
                      }
        query_string = urlencode(query_dict)
        url = "https://twitter.com/search?" + query_string
        return url

    def scrape(self):

        #first-page
        self.driver.get(self.first_page_url())

        scroll_num = 0

        #ajax
        while scroll_num < self.scroll_limit:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            scroll_num +=1

        page_source = self.driver.page_source
        self.driver.quit()

        return self.get_tweets_from_html(page_source)

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
