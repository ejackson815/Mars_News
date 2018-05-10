
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd
import shutil
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def init_browser():   
    #splintering
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome',**executable_path)


# In[2]:


# Initialize Pymongo to work with MongoDBs
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)


# In[3]:


#Define database & Collection
#db = client.marsnews_db
#collection = db.items

def scrape():
    print("Executing Scrape")
    print("----------")
    browser = init_browser()
    #Dict to hold all scraped data
    mars_data = {}
    # ### Mars News

    # In[4]:


    #Url of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    #Retrieve page with the requests module
    html = browser.html
    # Create BS4 object; parse with parser
    soup = BeautifulSoup(html,'html.parser')

    # save the most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    print(news_date)
    print(news_title)
    print(news_p)


    # #### couldn't get date function working
    # #Obtain Header and Paragraph text
    # #article = soup.find('div', class_='list_text')
    # #news_title = soup.find('div', 'content_title', 'a').text
    # #news_p = soup.find('div', 'rollover_description_inner').text
    # #news_date = article.find('div', class_='list_date').text
    # 

    # ### Space Images

    # In[5]:



    # url of page to be scraped
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    #html object
    html = browser.html

    #Parse HTML object with Beautiful Soup
    soup = BeautifulSoup(html,'html.parser')

    #capturing feature image
    image = soup.find('img', class_='thumb')['src']
    image_url = "http://jpl.nasa.gov"+image
    featured_image_url = image_url

    #download image as a JPG file
    response = requests.get(image_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


    # ### Mars Weather

    # In[6]:


    #import twitter dependacies & API Credentials
    import tweepy
    from config import consumer_key
    from config import sconsumer_key
    from config import access_token
    from config import saccess_token


    # In[7]:


    #Tweepy API Authorizations
    auth = tweepy.OAuthHandler(consumer_key, sconsumer_key)
    auth.set_access_token(access_token, saccess_token)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    #Target User
    target_user = '@MarsWxReport'
    #Obtain Tweet
    tweet = api.user_timeline(target_user, count = 1)
    mars_weather = tweet[0]['text']
    mars_weather


    # ### Mars Facts

    # In[8]:


    #Mars Facts Url for scrapping
    url3 = "http://space-facts.com/mars/"
    browser.visit(url3)


    # In[9]:


    #DataFrame Creation
    pull=pd.read_html(url3)
    mars_data_df=pd.DataFrame(pull[0])
    mars_data_df.columns=['Mars','Data']
    mars_table=mars_data_df.set_index("Mars")
    marsdata_df = mars_table.to_html(classes='marsdf')
    marsdata_df=marsdata_df.replace('\n', ' ')
    marsdata_df


    # ### Mars Hemispheres

    # In[10]:


    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    #reset
    hem_img_url = []


    # #### Valles Marineris

    # In[11]:


    #Move through pages
    time.sleep(5)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    time.sleep(5)

    #BS4 object parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #hold link
    vall_mar = soup.find('div','downloads').a['href']

    #create dictionary
    valles_marineris = {
        'title' : 'Valles Marineris Hemisphere',
        'img_url' : 'vall_mar'
    }

    #Append to Dict
    hem_img_url.append(valles_marineris)


    # #### Cerberus

    # In[12]:


    #Reset Url
    browser.visit(url4)
    #Move through pages
    time.sleep(5)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    time.sleep(5)

    #BS4 object parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #hold link
    cerb = soup.find('div','downloads').a['href']

    #create dictionary
    cerberus = {
        'title' : 'Valles Marineris Hemisphere',
        'img_url' : 'cerb'
    }

    #Append to Dict
    hem_img_url.append(cerberus)


    # #### Schiaparelli

    # In[13]:


    #Reset Url
    browser.visit(url4)
    #Move through pages
    time.sleep(5)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    time.sleep(5)

    #BS4 object parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #hold link
    sch = soup.find('div','downloads').a['href']

    #create dictionary
    schiaparelli = {
        'title' : 'Schiaparelli Hemisphere',
        'img_url' : 'sch'
    }

    #Append to Dict
    hem_img_url.append(schiaparelli)


    # #### Syrtis Major

    # In[14]:


    #Reset Url
    browser.visit(url4)
    #Move through pages
    time.sleep(5)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    time.sleep(5)

    #BS4 object parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #hold link
    syr_mjr = soup.find('div','downloads').a['href']

    #create dictionary
    syrtis_major = {
        'title' : 'Syrtis Major Hemisphere',
        'img_url' : 'syr_mjr'
    }

    #Append to Dict
    hem_img_url.append(syrtis_major)


    # In[15]:
    
    hem_img_url

    mars_data['hem_img_url'] = hem_img_url

    print("SUCCESS")
    return mars_data

