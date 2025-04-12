from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import itertools
import pandas as pd
import re
import emoji
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import language_tool_python
import random
import os

tool = language_tool_python.LanguageTool('en-US')
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

#parameters
number_of_tweets = 50000

keywords = [
    "suicide", "anxious", "kill", "can't sleep", "dipressed",
    "tired", "lonely", "hopeless", "never think talk", "stressed "
    "overdose of substance", "took too many pills", "took drug"
]

keywords = [k.strip() for k in keywords]

# Get all combinations of 2
keyword_combination = list(itertools.combinations(keywords, 3))

search_keys = []

for word in keyword_combination:
    sentence = word[0] + " OR " + word[1] + " OR " + word[2]
    search_keys.append(sentence)
    


print(search_keys)

exclusions = [
    "rt", "ai", "trade", "goated",
    "trump", "biden", "election", "modi", "tariffs", "republicans", "democrats",
    "crypto", "stockmarket", "bitcoin", "ceo", "stock", "economy", "recession",
    "lawsuit"]

#top 30 most populated except china
countries = ["IN", "US", "ID", "PK", "NG", "BR", "BD", "RU", "MX",
 "JP", "ET", "PH", "EG", "VN", "CD", "TR", "IR", "DE", "TH",
 "FR", "GB", "IT", "TZ", "ZA", "MM", "KE", "KR", "CO", "ES", "UA"]




options = Options()
options.binary_location = "/usr/bin/chromium-browser"
service1 = Service(executable_path=r"/home/nuke/chromedriver-linux64/chromedriver")

driver = webdriver.Chrome(service=service1)


"""
def profile_location(username):

    username = username.replace("@", "")
    driver.get(f"https://x.com/{username}")
    profile_location_element = driver.find_element(By.XPATH, value="//span[@data-testid='UserLocation']/span")

    return profile_location_element.text

"""

def clean_text(text):
    text = emoji.replace_emoji(text, replace=" ")  # Remove emojis
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", " ", text)  # Remove special characters
    text = " ".join([word.lower() for word in text.split() if word.lower() not in STOPWORDS])
    return text

driver.get("https://x.com/i/flow/login")
time.sleep(10)
username = driver.find_element(By.NAME, value="text")
next_button = driver.find_element(By.XPATH, value="//button[.//span[text()='Next']]")

username.send_keys("createcontent.nuke@gmail.com")
next_button.click()

time.sleep(7)

    #verification in loging-in
verification_input = driver.find_element(By.XPATH, value="//input[@name='text']")
next_button_2 = driver.find_element(By.XPATH, value="//button[.//span[text()='Next']]")

    #sending keys to verification
verification_input.send_keys("nileshpand309")
next_button_2.click()

time.sleep(7)

    #password 
password = driver.find_element(By.XPATH, value="//input[@name='password']")

login_buttot = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    #passing password
password.send_keys("Nilesh@325a")


login_buttot.click()

time.sleep(10)

tweets_list = []
possible_origin_country = []
tweet_user_id = []
tweet_total_reply = []
tweet_total_retweets = []
tweet_date_time = []
tweet_total_views = []
tweet_total_likes = []

for search_string in search_keys:
    for country in countries:

        query = f"I'm {search_string} country:{country}"
        driver.get(f"https://x.com/search?q={query}&src=typed_query&f=top")
        time.sleep(20)

        tweets = driver.find_elements(By.XPATH, '//article[@role="article" and @data-testid="tweet"]')

        for tweet in tweets:
            try:
                tweet_text_elements = tweet.find_elements(By.XPATH, './/div[@dir="auto"]')
                tweet_text = ' '.join([el.text for el in tweet_text_elements if el.text.strip() != ""])
                tweet_text = clean_text(tweet_text)
            except Exception as e:
                print("Exception in tweet text: ", e)
                tweet_text = "NA"
            tweets_list.append(tweet_text)

            try:
                tweet_username = tweet.find_element(By.XPATH, ".//a[@role='link' and starts-with(@href, '/')]/div//span[starts-with(text(), '@')]").text
            except:
                tweet_username = "NA"
            tweet_user_id.append(tweet_username)

            try:
                tweet_dt = tweet.find_element(By.XPATH, value=".//time[@datetime]").text
            except:
                tweet_dt = "NA"
            tweet_date_time.append(tweet_dt)

            try:
                replies = tweet.find_element(By.XPATH, value=".//button[@data-testid='reply']").text
            except:
                replies = "NA"
            tweet_total_reply.append(replies)

            try:
                retweets = tweet.find_element(By.XPATH, value=".//button[@data-testid='retweet']").text
            except:
                retweets = "NA"
            tweet_total_retweets.append(retweets)

            try:
                views = tweet.find_element(By.XPATH, ".//a[contains(@href, '/analytics') and @aria-label[contains(., 'views')]]").text
            except:
                views = "NA"
            tweet_total_views.append(views)

            # You can similarly extract likes or other metrics if available

# After collecting data, create the DataFrame safely
            print(len(tweets_list), len(tweet_user_id), len(tweet_date_time))  # Sanity check

            tw_data = {
                "tweet": tweets_list,
                "user": tweet_user_id,
                "date_time": tweet_date_time,
                "replies": tweet_total_reply,
                "retweets": tweet_total_retweets,
                "views": tweet_total_views,
                "country": country
            }


            df = pd.DataFrame(tw_data)
            #file_exists = os.path.isfile("data.csv")
            df.to_csv("x_data.csv", mode='a', index=False, header=False)


            time.sleep(random.randint(1, 3))

                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #.//button[@data-testid='reply'] reply element
                #//button[@data-testid='retweet'] retweets
                #//button[@data-testid='like'] likes
                #.//a[contains(@href, '/analytics') and @aria-label[contains(., 'views')]]




    #time.sleep(random.randint(2, 5))


print("---COMPLETED---")
time.sleep(50)

