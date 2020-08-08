#!/usr/bin/env python
# coding: utf-8

# In[1]:

def scrape():
    from bs4 import BeautifulSoup as bs 
    from splinter import Browser
    import requests
    import pandas as pd
    from twitter_scraper import get_tweets
    from twitterscraper import query_tweets


    # In[2]:


    executable_path = {'executable_path':'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # # Nasa Mars News

    # In[3]:


    nasa_mars_news_url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    news_response = requests.get(nasa_mars_news_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(news_response.text, 'html.parser')


    # In[4]:


    #Display the result to figure out what you want to scrape
    print(soup.prettify())


    # In[5]:


    # results are returned as an iterable list
    results = soup.find_all(class_="slide")
    titles_list = []
    paragraphs_list = []
    # Loop through returned results
    for result in results:
        # Error handling
        try:
            #Find title and paragraph for each link. The title is found within the second link in each slide, the paragraph
            #is found inside an inner description div tag.
            links = result.find_all('a')
            title = links[1].text
            paragraph = result.find(class_="rollover_description_inner").text
            #Append both to a list
            titles_list.append(title)
            paragraphs_list.append(paragraph)
        except AttributeError as e:
            print(e)


    # In[6]:


    #Save the first title and body into variables for use later
    news_title = titles_list[0]
    news_p = paragraphs_list[0]
    print(news_title)
    print(news_p)


    # # JPL Mars Space Images 

    # In[7]:


    #Second Web Scrape for Mars Image
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page with the requests module
    image_response = requests.get(mars_image_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(image_response.text, 'html.parser')
    # Examine the results
    print(soup.prettify())


    # In[8]:


    # results are returned as an iterable list
    results = soup.find_all(class_="carousel_items")
    # Loop through returned results
    for result in results:
        # Error handling
        try:
            #Find article tag and note that the link is in the 'style' parameter
            article = result.find('article', class_="carousel_item")
            article_link = article['style']
            #Use modification to fix the link to be in the correct format
            cleaned_article_link = article['style'].lstrip('background-image: url(')
            cleaned_article_link = cleaned_article_link.rstrip(');')
        except AttributeError as e:
            print(e)


    # In[9]:


    #Remove single quotes from the start and end of the string and then construct the image url
    cleaned_article_link = cleaned_article_link.replace("'", "")
    featured_image_link = 'https://www.jpl.nasa.gov'+cleaned_article_link
    #Print image url as a test
    print(featured_image_link)


    # # Mars Weather 

    # In[10]:


    #Third Web Scrape for Mars Weather Tweet
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    weather_response = requests.get(mars_twitter)
    browser.visit(mars_twitter)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(weather_response.text, 'html.parser')
    # Examine the results
    print(soup.prettify())


    # In[11]:


    # Scrap Tweets from MarsWxReport
    mars_tweets = []
    for tweet in get_tweets('MarsWxReport', pages=1):
        mars_tweets.append(tweet) # Add values to the list

    # Extract the weather value of the latest MarsWxReport Tweet
    mars_weather_dict = {}
    mars_weather_dict = mars_tweets[0]
    mars_weather = mars_weather_dict.get('text')
    print('The latest Mars Weather Report is: ' + mars_weather)


    # # Mars Facts

    # In[12]:


    mars_facts_url = "https://space-facts.com/mars/"
    #Scrape using pandas
    facts_table = pd.read_html(mars_facts_url)
    facts_table


    # # Mars Hepispheres

    # In[13]:


    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
        print(title)
        print(image_url)

    return (scraped_dict)




