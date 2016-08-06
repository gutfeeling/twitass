import time
import json
import warnings

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

warnings.filterwarnings('ignore')

class AdvancedSearchScraper(object):

    def __init__(self, all_of_these_words, limit = 100):
        self.all_of_these_words = all_of_these_words
        if limit:
            self.limit = limit
        else:
            self.limit = float("inf")

    def first_page_params(self):
        query_dict = {"src" : "typd",
                      "q" : self.all_of_these_words,
                      "f" : "tweets",
                      }
        return query_dict

    def ajax_call_params(self, oldest_tweet_id, newest_tweet_id):
        query_dict = {"src" : "typd",
                      "q" : self.all_of_these_words,
                      "f" : "tweets",
                      "include_available_features" : 1,
                      "include_entities" : 1,
                      "reset_error_state" : "false",
                      "max_position" : "TWEET-%s-%s" %(oldest_tweet_id, newest_tweet_id),
                      }
        return query_dict

    def scrape(self):
        self.tweets = []

        #first-page
        response = requests.get("https://twitter.com/search",
                                params = self.first_page_params(),
                                verify = False)
        self.tweets+=self.get_tweets_from_html(response.text)

        #ajax
        if len(self.tweets)>0:

            newest_tweet_id = self.tweets[0]['tweet_id']
            oldest_tweet_id = self.tweets[-1]['tweet_id']

            while len(self.tweets) < self.limit:

                time.sleep(5)

                response = requests.get("https://twitter.com/i/search/timeline",
                                        params = self.ajax_call_params(
                                            oldest_tweet_id, newest_tweet_id),
                                        verify = False)
                json_data = json.loads(response.text)
                self.tweets+=self.get_tweets_from_html(json_data["items_html"])

                if oldest_tweet_id == self.tweets[-1]['tweet_id']:
                    break

                oldest_tweet_id = self.tweets[-1]['tweet_id']

        return self.tweets





    def get_tweets_from_html(self, html_doc):
        tweetlist = []
        html_soup = BeautifulSoup(html_doc, "html.parser")
        tweet_soup_list = html_soup.find_all("div", {"class" : "original-tweet"})
        for tweet_soup in tweet_soup_list:
            try:
                tweet_dict = {
                    "tweet_id" : int(tweet_soup["data-tweet-id"]),
                    "author_name" : tweet_soup["data-name"],
                    "author_handle" : tweet_soup["data-screen-name"],
                    "author_id" : int(tweet_soup["data-user-id"]),
                    "author_href" : tweet_soup.find("a",{"class" : "account-group"})["href"],
                    "tweet_permalink" : tweet_soup["data-permalink-path"],
                    "tweet_text" : self.prettify_tweet_text_bs_element(
                                       tweet_soup.find("p", {"class" : "tweet-text"})),
                    "tweet_language" : tweet_soup.find("p", {"class" : "tweet-text"})['lang'],
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
            except Exception as e:
                print("Error while extracting information from tweet.\n")
                print(e)
        return tweetlist

    def prettify_tweet_text_bs_element(self, tweet_text_bs_element):
        tweet_text = ''
        for child in tweet_text_bs_element.children:
            if isinstance(child, NavigableString):
                tweet_text += child + " "
            elif isinstance(child, Tag):
                try:
                    tag_class = child['class'][0]
                    if tag_class == "twitter-atreply":
                        mention = ''.join([i.string for i in child.contents])
                        tweet_text += mention + " "
                    elif tag_class == "twitter-hashtag":
                        hashtag = ''.join([i.string for i in child.contents])
                        tweet_text += hashtag + " "
                    elif tag_class == "twitter-timeline-link":
                        if isinstance(child["href"], str):
                            tweet_text += child["href"] + " "
                except:
                    if isinstance(child.string, str):
                        tweet_text += child.string + " "
        return " ".join(tweet_text.split())
