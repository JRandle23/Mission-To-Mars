from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests 
import pandas as pd 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

    

def scrape():
    browser = init_browser()
    
    mars_info = {}

## Mars News
    
    # Set NASA Mars news url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    first_story = soup.find('li', class_='slide')
    news_title = first_story.find('div', class_='content_title').text
    news_p = first_story.find('div', class_='article_teaser_body').text

    mars_info["News Title"] = news_title
    mars_info["News Paragraph"] = news_p

## JPL Mars Images - Featured Image

    # Set URL path 
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Navigate webpage to find image URL
    img = browser.click_link_by_partial_text("FULL IMAGE")
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space'
    img_url = browser.find_by_css('img.fancybox-image')['src']
    featured_image_url = base_url + img_url
    
    mars_info["Featured Image"] = featured_image_url

## Mars Facts

    # Set URL path and read in html
    url = "https://space-facts.com/mars/"

    facts_table = pd.read_html(url)

    # Convert table into data frame
    mars_facts = facts_table[0]
    mars_facts.rename(columns={0: 'Description', 1: 'Mars'}, inplace=True)
    
    # Convert table into html string
    mars_facts_table_string = mars_facts.to_html(index=False, header=False)

    mars_info["Table Facts HTML"] = mars_facts_table_string


## Mars Hemispheres 

    # Hemisphere home link
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    base_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for h in hemispheres: 
    # Store title
        title = h.find('h3').text
    
    # Store link that leads to full image website
        partial_img_url = h.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
        browser.visit(base_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
        img_url = base_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info["Hemisphere Image URLS"] = hemisphere_image_urls
    
    browser.quit()
    
    return mars_info 







