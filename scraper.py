import time
import json
import warnings

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

warnings.filterwarnings('ignore')

class AdvancedSearchScraper(object):

    """AdvancedSearchScraper(query, limit = 100)
    This class scrapes tweets from the Twitter Advanced Search results page

    Explanation of parameters:

    - query

      If you want to perform the search
      https://twitter.com/search?q=python%20lang%3Aen%20since%3A2016-08-01%20&src=typd,
      then you should use:

      ass = AdvancedSearchScraper("python%20lang%3Aen%20since%3A2016-08-01%20")

      Forming the correct query is your responsibility!!!

      Please play with the page https://twitter.com/search-advanced to learn
      how queries should be formed!

      Note that the class will automatically take care of all other url parameters
      like "src" etc.

    - limit

      limit indicates the approximate number of tweets that should be scraped.
      The default value is 100. Set it to None if you want to scrape all tweets.
    """

    def __init__(self, query, limit = 100):

        # We could have used separate parameters like language, since, until
        # Corresponding to each form element in the Advanced Search page.
        # But this complicates the logic of the class.
        # We would have to validate the parameters and this is messy.
        # We would also have to form the query, which is messy too.
        # We choose elegance instead, and leave the job of forming the
        # correct query to the user.

        self.query = query
        if limit:
            self.limit = limit
        else:
            self.limit = float("inf")


    def ajax_call_params(self, oldest_tweet_id, newest_tweet_id):
        query_dict = {"src" : "typd",
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

        # if q is supplied in the params dictionary, requests replaces
        # spaces by + . this results in an unexpected final url.
        # this is the only way to form the correct url.
        response = requests.get("https://twitter.com/search?q=%s" % self.query,
                                params = {"src" : "typd", "f" : "tweets"},
                                verify = False)
        self.tweets+=self.get_tweets_from_html(response.text)

        #ajax
        if len(self.tweets)>0:

            newest_tweet_id = self.tweets[0]['tweet_id']
            oldest_tweet_id = self.tweets[-1]['tweet_id']

            while len(self.tweets) <= self.limit:

                # rate limiting! 1 AJAX call in 5 seconds.

                time.sleep(5)

                # if q is supplied in the params dictionary, requests replaces
                # spaces by + . this results in an unexpected final url.
                # this is the only way to form the correct url

                response = requests.get(
                    "https://twitter.com/i/search/timeline?q=%s" % self.query,
                    params = self.ajax_call_params(oldest_tweet_id, newest_tweet_id),
                    verify = False)
                json_data = json.loads(response.text)
                self.tweets+=self.get_tweets_from_html(json_data["items_html"])

                if oldest_tweet_id == self.tweets[-1]['tweet_id']:
                    break

                oldest_tweet_id = self.tweets[-1]['tweet_id']

        if isinstance(self.limit, int):
            return self.tweets[:self.limit]

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