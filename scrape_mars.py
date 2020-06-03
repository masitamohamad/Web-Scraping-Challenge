from splinter import Browser
from bs4 import BeautifulSoup as bs 
import pandas as pd 
import requests 
from selenium import webdriver
import time


def scrape():

    ###########################################################################################
    # NASA Mars News
    ###########################################################################################

    response = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest").text
    soup = bs(response, 'html.parser')
    news_parent = soup.find_all('div', class_='slide')
    news_title = soup.find_all('div', class_='content_title')
    latest_news_title = news_title[0].a.text
    news_paragraph= soup.find_all('div', class_='rollover_description_inner')
    latest_news_paragraph = news_paragraph[0].get_text()

    print("---------------NASA Mars News Scraping Complete!---------------")

    ##########################################################################################
    # JPL Mars Space Images
    ##########################################################################################

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)
    current_html = browser.html
    image_soup = bs(current_html, 'html.parser')
    partial_img_url = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = "https://www.jpl.nasa.gov" + partial_img_url
    browser.quit()

    print("---------------JPL Mars Space Images Scraping Complete!---------------")

    ###########################################################################################
    # Mars Weather
    ###########################################################################################

    driver = webdriver.Chrome()
    driver.get('https://twitter.com/marswxreport?lang=en')
    time.sleep(5)
    html = driver.page_source
    twitter_soup = bs(html, 'html.parser')
    latest_tweets = twitter_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    driver.close()
    tweet_list = []
    for tweet in latest_tweets:
        tweet_list.append(tweet.text)

    keyword = 'InSight'
    weather_tweet = [i for i in tweet_list if keyword in i] 
    mars_weather = weather_tweet[0]

    print("---------------Mars Weather Scraping Complete!---------------")

    ###########################################################################################
    # Mars Facts
    ###########################################################################################

    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Description','Value']
    mars_facts_df.set_index('Description', inplace=True)

    print("---------------Mars Facts Scraping Complete!---------------")

    ###########################################################################################
    # Mars Hemispheres
    ###########################################################################################
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(3)
    html_hemispheres = browser.html

    hemisphere_soup = bs(html_hemispheres, 'html.parser')
    items = hemisphere_soup.find_all('div', class_='item')

    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        hemisphere_img_html = browser.html
             
        hemisphere_img_soup = bs(hemisphere_img_html, 'html.parser')
        
        img_url = hemispheres_main_url + hemisphere_img_soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
 
    browser.quit()

    print("---------------Mars Hemispheres Scraping Complete!---------------")

    ###########################################################################################
    # Store the return value in Python dictionary
    ###########################################################################################

    mars_data_dict = {}

    mars_data_dict['news_title'] = latest_news_title
    mars_data_dict['news_paragraph'] = latest_news_paragraph
    mars_data_dict['featured_image_url'] = featured_image_url
    mars_data_dict['mars_weather'] = mars_weather

    mars_facts = mars_facts_df.to_html(header=True, index=True)
    mars_data_dict['mars_facts'] = mars_facts

    mars_data_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data_dict
