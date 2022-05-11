'''
    PROJECT : Price Comparator
    
    FILENAME : amazon_ca.py

    DESCRIPTION :
        This program takes the information gathered from selected websites 
        and stores them in JSON files.
    
    FUNCTIONS :
        get_content_data()
        get_product_urls()
        get_product_data()
        set_product_data()


    NOTES :
        Need to fix random scrape failures. Unsure what is causing them.
        Might have something to do with the browser session and javascript.
        
    AUTHOR :    Noah Arcand Da Silva    START DATE :    2021.03.07 (YYYY-MM-DD)

    CHANGES :
        1. Updated HTML class/id naming conventions.
        2. Merged browser sessions into one file.
    
    VERSION     DATE        WHO     DETAIL
    0.0.1b      2022.05.11  Noah    Project refresh to work with newer libraries.
'''

from bs4 import BeautifulSoup    # BeautifulSoup helps us find the tags we need in the HTML of the website.
import requests    # Requests allows us to access and pull the website's HTML.

from selenium import webdriver    # The web drivers from selenium lets us access the website with the browser of our choice.
from webdriver_manager.firefox import GeckoDriverManager    # Automates the executable path management part of selenium.

firefox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())    # Open a browser session.

class AmazonCA(object):
    def __init__(self, item):                                                                         # Making the search result URL with the name of the item
        self.search_url = (f'https://www.amazon.ca/s?k={item}').replace(' ', '+')    # to search. Replacing spaces in the item name with '+'.

    def get_content_data(self):    # Function to collect content/data from the search URL.
        firefox_driver.get(self.search_url)    # Make a GET request to amazon.ca/..., using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content.

    def get_product_urls(self):    
        # Filtering the product URL from what we got in the getContentData() function:
        page_data = self.get_content_data().find_all('div', class_=
            'a-section a-spacing-none a-spacing-top-small s-title-instructions-style')    # Getting all the products inside the DIV block (mostly search results, mix of sponsored).
        #print(len(productLinks))
        page_links = []
        for i in page_data:    # Going through each product in the DIV block.
            page_links.append(i.h2.a['href'])    # Add the URL paths to the pageLink list (amazon product links only contain the path to the store, and not a full link).
        product_links = ['https://www.amazon.ca' + i 
            for i in page_links if not i.startswith('/gp/')]    # Filter out the sponsored content (starts with /gp/), and add the domain in front of the URL path.

        refined_links = []    # New list to put non-duplicate URLs.
        for i in product_links:    # Going through each product URL in the list.
            if i not in refined_links:    # Checking to see if the URL is already in the refined_links list
                refined_links.append(i)    # If they aren't already there, add them.
        
        return refined_links    # Returns the list of product URLs.

    def get_product_data(self, url):    # Function to collect product information from the product URL.
        firefox_driver.get(url)    # Make a GET request to the site URL, using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content

    def set_product_data(self):    # Filtering specific data about the product from what we got in the getData() function:
        product_info_list = []    # Where we'll store all of the products' data.
        product_brand,product_model,product_title,product_price,product_rating,product_review_count = 'NONE','NONE','NONE','NONE','NONE','NONE'    # Initializing each product variable.
        
        
        url_listfull = self.get_product_urls()    # Store the URL list from getProductURLs() into URL_LIST.
        url_list = url_listfull[:3]


        for url in url_list:    # For each URL in the URL_LIST:
            product_data = self.get_product_data(url)    # Pull all the data from the product page.
            
            try:    # Grab the product Brand as a string.               
                for th_tag in product_data.find_all('th', class_='a-color-secondary a-size-base prodDetSectionEntry'):    # Find all HTML th tags on the page.
                    if th_tag.text.strip() == 'Brand':    # Filter the tag with name 'Brand'
                        product_brand = th_tag.find_next_sibling().text.strip()    # Store the next sibling (brand name) into productBrand.
            except:
                product_brand = "NONE"    # If it can't find a brand name, set the value to NONE.

            try:    # Grab the Model as a string, and replace the unwanted section with nothing.
                for th_tag in product_data.find_all('th', class_='a-color-secondary a-size-base prodDetSectionEntry'):    # Find all HTML th tags on the page.
                    if th_tag.text.strip() == 'Item model number':    # Filter the tag with name 'Item model number'
                        product_model = th_tag.find_next_sibling().text.strip()    # Store the next sibling (model number) into productModel.
            except:
                product_model = "NONE"    # If it can't find a model number, set the value to NONE.

            try:    # Grab the Title as a string.
                product_title = product_data.find('span', class_='a-size-large product-title-word-break').text.strip()
            except:
                product_title = "NONE"    # If it can't find a title, set the value to NONE.

            try:    # Grab th Price as a string.
                whole_price = product_data.find('span', class_='a-price-whole').text.strip()
                faction_price = product_data.find('span', class_='a-price-fraction').text.strip()
                product_price = whole_price + faction_price
            except:
                product_price = "NONE"    # If it can't find a price, set the value to NONE.

            try:    # Reviews has error handling in case there isn't any reviews. 
                product_rating = product_data.find('span', class_='a-icon-alt').text.strip()    # Grab the Rating as a string.
                product_review_count = product_data.find('span', id='acrCustomerReviewText').text.strip()    # Grab the number of Reviews as a strings.
            except:
                product_rating = "NONE"    # If it can't find any reviews, set the value to NONE.
                product_review_count = "NONE"     # If it can't find any reviews, set the value to NONE.

            product_brand = product_brand.replace(u'\xa0', u'')
            product_brand = product_brand.replace(u'\u200e', '')
            product_model = product_model.replace(u'\xa0', u'')
            product_model = product_model.replace(u'\u200e', '')
            product_price = product_price.replace(u'\xa0', u'')
            product_rating = product_rating.replace(' out of 5 stars', '')
            product_review_count = product_review_count.replace(' ratings', '')

            product_info = {    # Create a dictionary with the product's collected data.
                'brand': product_brand,
                'model': product_model,
                'title': product_title,
                'price': product_price,
                'rating': product_rating,
                'num of reviews': product_review_count
                }
            
            product_info_list.append(product_info)    # Add the productInfo dictionary to the list.

        firefox_driver.close()

        return product_info_list    # Return the list of dictionaries.