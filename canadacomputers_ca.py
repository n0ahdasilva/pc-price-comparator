'''
    PROJECT : Price Comparator
    
    FILENAME : canadacomputers_ca.py

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
    
        (C) 2022 n0ahdasilva. All rights reserved.
    
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

class CanadaComputersCA(object):

    def __init__(self, item):                                                                                                             # Making the search result URL with the name of the item
        self.search_url = (f'https://www.canadacomputers.com/search/results_details.php?language=en&keywords={item}').replace(' ', '+')    # to search. Replacing spaces in the item name with '+'.

    def get_content_data(self):    # Function to collect content/data from the search URL.
        firefox_driver.get(self.search_url)    # Make a GET request to canadacomputers.com/..., using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content.

    def get_product_urls(self):    
        # Filtering the product URL from what we got in the getContentData() function:
        all_links = [a['href'] for a in self.get_content_data().find_all('a', href=True)]    # Grab all the URLs from href values on the page.
        product_links = [i for i in all_links if i.startswith('https://www.canadacomputers.com/product_info.php?')]    # Filter them by product links.

        refined_links = []    # New list to put non-duplicate URLs.
        for i in product_links:    # Going through each product URL in the list.
            if i not in refined_links:    # Checking to see if the URL is already in the refinedLinks list
                refined_links.append(i)    # If they aren't already there, add them.

        return refined_links    # Returns the list of product URLs.

    def get_product_data(self, url):    # Function to collect product information from the product URL.
        firefox_driver.get(url)    # Make a GET request to URL, using Selenium.
        soup = BeautifulSoup(firefox_driver.page_source, 'lxml')    # Collect all the content from the page.
        return soup    # Returns that content

    def set_product_data(self):    # Filtering specific data about the product from what we got in the getData() function:
        product_info_list = []    # Where we'll store all of the products' data.
        product_brand,product_model,product_title,product_price,product_rating,product_review_count = 'NONE','NONE','NONE','NONE','NONE','NONE'    # Initializing each product variable.
        url_list = self.get_product_urls()    # Store the URL list from getProductURLs() into URL_LIST.

        for url in url_list:    # For each URL in the URL_LIST:
            product_data = self.get_product_data(url)    # Pull all the data from the product page.

            try:    # Grab the product Brand as a string.
                product_brand = product_data.find('a', class_='text-cc').text.strip()
            except:
                product_brand = "NONE"    # If it can't find a brand name, set the value to NONE.
                
            try:    # Grab the Model as a string, and replace the unwanted section with nothing.
                product_model = product_data.find('div', class_='col-auto ml-auto').text.strip()
            except:
                product_model = "NONE"    # If it can't find a model number, set the value to NONE.
                
            try:    # Grab the Title as a string.
                product_title = product_data.find('h1', class_='h3 mb-0').text.strip()
            except:
                product_title = "NONE"    # If it can't find a title, set the value to NONE.

            try:    # Grab th Price as a string.
                product_price = product_data.find('span', class_='h2-big').text.strip()
            except:
                product_price = "NONE"    # If it can't find a price, set the value to NONE.

            try:    # Reviews has error handling in case there isn't any reviews. 
                product_rating = product_data.find('span', class_='h3 mt-0_5').text.strip()    # Grab the Rating as a string.
                productReviewCount = (product_data.find('a', class_='text-underline').text.strip())    # Grab the number of Reviews as a strings.
            except:
                product_rating = "NONE"    # If it can't find any reviews, set the value to NONE.
                product_review_count = "NONE"     # If it can't find any reviews, set the value to NONE.

            product_model = product_model.replace("Part #: ", '')
            product_price = product_price.replace('$', '')
            product_review_count = product_review_count.replace(' Reviews', '')

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