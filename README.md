# TwitterScripts

## scrape_pics.py

* `python scrape_pics.py twitterusername1 twitterusername2 ...etc`
* This will scrape all the images from the twitter accounts passed in as command line arguments, with 5-minute breaks between each account so as not to exceed the Twitter API rate limit. 
* All images are stored in a `./pics` folder inside this repo, organized by twitter user.
* Useful for backing up your photos before deleting your account, or getting tons of images from your favorite accounts to use as e.g. rotating screensavers, or to display on your TV with chromecast.
