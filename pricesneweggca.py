# Noah Arcand Da Silva
# 2021-03-07 (YYYY-MM-DD)
# Price Comparator - pricesnewegg.py
# Version 1.0

""" NOTE — ABOUT THIS PROGRAM 
...
"""

from bs4 import BeautifulSoup    # BeautifulSoup helps us find the tags we need in the HTML of the website.
import requests    # Requests allows us to access and pull the website's HTML.
from selenium import webdriver    # The web drivers from selenium lets us access the website with the browser of our choice.
from webdriver_manager.firefox import GeckoDriverManager    # Automates the executable path management part of selenium.

firefox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())    # Open a browser session.

class NeweggCA(object):
    def __init__(self, item):                                                           # Making the search result URL with the name of the item
        self.search_url = (f'https://www.newegg.ca/p/pl?d={item}').replace(' ', '+')    # to search. Replacing spaces in the item name with '+'.

    def get_content_data(self):    # Function to collect content/data from the search URL.
        firefox_driver.get(self.search_url)    # Make a GET request to newegg.ca/..., using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content.

    def get_product_urls(self):    
        # Filtering the product URL from what we got in the getContentData() function:
        all_links = [a['href'] for a in self.get_content_data().find_all('a', href=True)]    # Grab all the URLs from href values on the page.
        product_links = [i for i in all_links if i.endswith('-_-Product')]    # Filter them by product links.

        refined_links = []    # New list to put non-duplicate URLs.
        for i in product_links:    # Going through each product URL in the list.
            if i not in refined_links:    # Checking to see if the URL is already in the refinedLinks list
                refined_links.append(i)    # If they aren't already there, add them.

        return refined_links    # Returns the list of product URLs.

    def get_product_data(self, url):    # Function to collect product information from the product URL.
        firefox_driver.get(url)    # Make a GET request to the site URL, using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content

    def set_product_data(self):    # Filtering specific data about the product from what we got in the getData() function:
        product_info_list = []    # Where we'll store all of the products' data.
        product_brand,product_model,product_title,product_price,product_rating,product_review_count = 'NONE','NONE','NONE','NONE','NONE','NONE'    # Initializing each product variable.
        url_list = self.get_product_urls()    # Store the URL list from getProductURLs() into URL_LIST.

        for url in url_list:    # For each URL in the URL_LIST:
            product_data = self.get_product_data(url)    # Pull all the data from the product page.
            
            try:    # Grab the product Brand as a string.
                for caption in product_data.find_all('caption'):    # Find all HTML caption tags on the page.
                    if caption.get_text() == 'Model':    # Filter those tags with name 'Model'
                        model_info_table = caption.find_parent('table', class_='table-horizontal')    # Store the table's data with the 'Model' caption inside modelTable.

                tr_tags = model_info_table.find_all('tr')    # Find all the 'tr's in the table's data (tr tags hold the data we're looking for).
                for tr_tag in tr_tags:    #   Look through each tr.modelTable
                    if not tr_tag.text.find("Brand"):    # Find the tr tag that contains Brand information.
                        product_brand = tr_tag.text.replace('Brand ', '', 1)    # Remove the 'Brand ' text that comes before the brand name, and store it.
            except:
                product_brand = "NONE"    # If it can't find a brand name, set the value to NONE.

            try:    # Grab the Model as a string, and replace the unwanted section with nothing.
                for caption in product_data.find_all('caption'):    # Find all HTML caption tags on the page.
                    if caption.get_text() == 'Model':    # Filter those tags with name 'Model'.
                        model_info_table = caption.find_parent('table', class_='table-horizontal')    # Store the table's data with the 'Model' caption inside modelTable.

                tr_tags = model_info_table.find_all('tr')    # Find all the 'tr's in the table's data (tr tags hold the data we're looking for).
                for tr_tag in tr_tags:   #   Look through each 'tr.modelTable'.
                    if not tr_tag.text.find("Model"):    # Find the tr tag that contains model information.
                        product_model = tr_tag.text.replace('Model ', '', 1)    # Remove the 'Model ' text that comes before the model name, and store it.            
            except:
                product_model = "NONE"    # If it can't find a model number, set the value to NONE.
                
            try:    # Grab the Title as a string.
                product_title = product_data.find('h1', class_='product-title').text.strip()
            except:
                product_title = "NONE"    # If it can't find a title, set the value to NONE.

            try:    # Grab th Price as a string.
                product_price = product_data.find('li', class_='price-current').text.strip()
            except:
                product_price = "NONE"    # If it can't find a price, set the value to NONE.

            try:    # Reviews has error handling in case there isn't any reviews. 
                product_review_info = product_data.find('div', class_=
                    'product-action-group display-flex align-items-center justify-content-space-between')    # Grab the Rating data.  
                
                product_rating_title = (product_review_info.find('i', class_=lambda value: value and value.startswith('rating rating-')))    # Grab the rating class from 1 to 5 stars.      
                product_rating = product_rating_title.get('title').strip()    # Get the title from the productRating class.
                product_review_count = product_review_info.find('span', class_='item-rating-num').text.strip()    # Grab the number of Reviews as a strings.
            except:
                product_rating_title = "NONE"    # If it can't find any reviews, set the value to NONE.
                product_review_count = "NONE"    # If it can't find any reviews, set the value to NONE.

            product_rating = product_rating.replace(' out of 5 eggs', '', 1)
            product_review_count = product_review_count.lstrip(' (').rstrip(') ')

            product_info = {    # Create a dictionary with the product's collected data.
                'brand': product_brand,
                'model': product_model,
                'title': product_title,
                'price': product_price,
                'rating': product_rating,
                'num of reviews': product_review_count
                }
            
            product_info_list.append(product_info)    # Add the productInfo dictionary to the list.

        return product_info_list    # Return the list of dictionaries.