import tweepy
import ipdb
import requests
from io import open as iopen
import os
import time
from ./secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, TOKEN_SECRET

# this method was adapted minorly from one written by Peter Hanley
# https://coderwall.com/p/lngdkg/saving-images-with-just-requests-http-for-humans
def save_img_from_url(file_url):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg',]
    file_name =  file_url.split('/')[-1]
    file_suffix = file_name.split('.')[1]
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == requests.codes.ok:
        with iopen(file_name, 'wb') as file:
            file.write(i.content)
    else:
        return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)
api = tweepy.API(auth)

twitter_handles = [
# your list of twitter handles to harvest for pics goes here
# "twitterUsername1",
# "twitterUsername2",
#  etc.
]
def get_images(twitter_handle):
    if not os.path.exists(twitter_handle):
        os.makedirs(twitter_handle)
        print("Created directory ./{}.".format(twitter_handle))
    os.chdir(twitter_handle)

    user = api.get_user(twitter_handle)
    urls = []
    pages = int(user.statuses_count / 20) + 1
    if pages > 165:
        pages = 165
    try:
        for x in range(pages):
            print("Scanning page {}/{}".format(x, pages))
            tl = api.user_timeline(user_id=user.id,page=x)
            for tweet in tl:
                if tweet.entities and 'media' in tweet.entities.keys():
                    for picture in tweet.entities['media']:
                        print(picture['media_url_https'])
                        urls += [picture['media_url_https']]
    except:
        print("Rate limit exceeded! Saving found photos...")
    ctr = 1
    err_ctr = 0
    length = len(urls)
    for url in urls:
        try:
            save_img_from_url(url)
            print("File saved! ({}/{})".format(ctr, length));
        except:
            print("ERROR: File download failed! Trying next...")
            err_ctr += 1
            print("Errors so far: {}".format(err_ctr))
        ctr += 1

    print("Total errors: {}".format(err_ctr))
    os.chdir('..') # return to the top level


if __name__ == "__main__":
    if not os.path.exists('pics'):
        os.makedirs('pics')
    os.chdir('pics')

    for t in twitter_handles:
        get_images(t)
        time.sleep(300)  # 5min between scrapes to prevent API rate limit issues
