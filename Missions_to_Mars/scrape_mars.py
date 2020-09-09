import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import os

def scrape_info():


    browser = Browser('chrome', executable_path="C:\\Users\\nprow\\Documents\\GitHub\\web-scraping-challenge\\Missions_to_Mars\\chromedriver.exe")
    mars = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all('div', class_='content_title')
    news_title[1].text

    mars["news_title"]=news_title[1].text

    news_p = soup.find('div', class_='article_teaser_body')
    news_p.text

    mars["news_p"]=news_p.text
    mars

    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id("full_image").click()
    time.sleep(1)
    browser.find_link_by_partial_text("more info").click()
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    result = soup.find('figure', class_="lede")
    link=result.a.img["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + link
    mars["featured_image"] = featured_image_url

    url = "https://space-facts.com/mars/"
    table=pd.read_html(url)
    df=table[0]
    df.columns=['Description', 'Values']
    html_table=df.to_html()
    html_table=html_table.replace('\n', '')
    mars["facts"] = html_table
    
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_url=[]
    links = browser.find_by_css("a.product-item h3")
    for link in range(len(links)):
        hemispheres={}
        browser.find_by_css("a.product-item h3")[link].click()
        element = browser.find_link_by_text('Sample').first
        hemispheres["img_url"]=element["href"]
        hemispheres["title"]=browser.find_by_css("h2.title").text
        hemisphere_image_url.append(hemispheres)
        browser.back()
    mars["hemisphere"] = hemisphere_image_url

    return mars