# Noah Arcand Da Silva
# 2021-03-07 (YYYY-MM-DD)
# Price Comparator - source.py
# Version 1.0

""" NOTE — ABOUT THIS PROGRAM 
This program takes the information gathered from selected websites and stores them in JSON 
files for later access.
"""

import json

# We've imported the other .py files used for individual store searching.
from pricesneweggca import *
from pricescanadacomputers import *
from pricesamazonca import *

#from browsersession import *

class JSONFiles(object):
    def __init__(self, item):
        self.file_name = (f'{item}.json').replace(' ', '_')    # Pulling the filename that we need depending on the website we currently use at the time.
    
    def load_file(self):
        with open(f'{self.file_name}.json', 'r') as fp:
            file_data = json.load(fp)

    def save_file(self):
        with open(f'{self.file_name}.json', 'w') as fp:
            json.dump(data, fp)

class ItemDataCA(object):
    def __init__(self, search_in):
        self.search_in = search_in
        self.search_for = search_for

    def data_canada(self):
        for site in self.search_in:    # Only searching for the site selected, instead of searching in all of them.
            """ NOTE: These are the Canadian sites.
            """
            if site == 'newegg.ca':    # Run the search on newegg.ca if it was selected.
                try:
                    price_newegg_ca = NeweggCA(self.search_for)    # Initialize the NeweggCA class with the correct search URL.
                    data_newegg_ca = price_newegg_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_newegg_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')
        
                if data_newegg_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    print()

            if site == 'canadacomputers.com':    # Run the search on canadacomputers.com if it was selected.
                try:
                    price_cc_ca = CanadaComputers(self.search_for)    # Initialize the CanadaComputers class with the correct search URL.
                    data_cc_ca = price_cc_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_cc_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')

                if data_newegg_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    print()

            if site == 'amazon.ca':    # Run the search on amazon.ca if it was selected.
                try:
                    price_amazon_ca = AmazonCA(self.search_for)    # Initialize the AmazonCA class with the correct search URL.
                    data_amazon_ca = price_amazon_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_amazon_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')
        
                if data_newegg_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    print()

search_sites = ['newegg.ca', 'amazon.ca', 'canadacomputers.com']    # List of all the sites we have in our program.

search_for = 'corsair case'    # Search term that the user wants to search for.
search_in = ['newegg.ca', 'canadacomputers.com']    # List of the sites that the user wants to search in.

test_run = ItemDataCA(search_in)
test_run.data_canada()