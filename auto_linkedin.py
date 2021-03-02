from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

# in order to not visit too many profiles and get banned
MAX_PROFILES = 100
MAX_GOOGLE_PAGES = 50

# store profile and password
config = {'username': 'fakeemail@google.com',
         'password': 'fakepassword'}

# open browser window
browser = webdriver.Chrome('chromedriver.exe')
browser.get('https://www.linkedin.com/login')

# enter username
username = browser.find_element_by_id('username')
username.send_keys(config['username'])

# enter password
password = browser.find_element_by_id('password')
password.send_keys(config['password'])

# place randomly sized sleeps throughout to not overload server with requests
sleep(random.random() * 3)

# login
login_button = browser.find_element_by_class_name('from__button--floating')
login_button.click()


linkedin_ulrs = []
for i in range(1,MAX_GOOGLE_PAGES+1):
    # fetch google
    browser.get('https://www.google.com/')
    sleep(random.random() * 3 + 2)

    # search for keywords we want in profiles
    search_query = browser.find_element_by_name('q')
    search_query.send_keys('site:cz.linkedin.com/in/ AND "Python developer Prague" ' + 'page' + ' ' + str(i))
    sleep(random.random() * 3 + 2)
    search_query.send_keys(Keys.RETURN)

    # grab urls from google page
    urls = browser.find_elements_by_xpath("//a[@href]")
    urls = [elem.get_attribute("href") for elem in urls]
    # filter out only linkedin urls
    urls = [elem for elem in urls if 'google' not in elem and 'https://cz.linkedin.com/in' in elem]
    sleep(1)

    # visit linkedin profiles
    for idx, url in enumerate(urls):
        # in case a profile comes up in google search repeatedly
        if url not in linkedin_ulrs:
            # in case we already visited the max number of profiles
            if len(linkedin_ulrs) >= MAX_PROFILES:
                break
            # add to visited profiles
            linkedin_ulrs.append(url)
            print(f'{idx}:\t{url}')
            sleep(random.random() * 10 + 2)
            browser.get(url)

    if len(linkedin_ulrs) >= MAX_PROFILES:
        print("max profiles exceeded")
        break

'''
Ideas for extension: automatically send contact request/message/scrape user info for recruiting purposes
'''
