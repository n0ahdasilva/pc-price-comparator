'''
    PROJECT : Price Comparator
    
    FILENAME : source.py

    DESCRIPTION :
        This program takes the information gathered from selected websites 
        and stores them in JSON files.
    
    FUNCTIONS :
        data_canada()
        main()

    NOTES :
        Need to fix random scrape failures. Unsure what is causing them.
        It might have something to do with the browser session and javascript.
        
    AUTHOR :    Noah Arcand Da Silva    START DATE :    2021.03.07 (YYYY-MM-DD)

    CHANGES :
        1. Updated HTML class/id naming conventions.
        2. Merged browser sessions into one file.
    
    VERSION     DATE        WHO     DETAIL
    0.0.1b      2022.05.11  Noah    Project refresh to work with newer libraries.
'''

import json

# We've imported the other .py files used for individual store searching.

from newegg_ca import *
from canadacomputers_ca import *
from amazon_ca import *
#from browsersession import *

class ItemDataCA(object):
    def __init__(self, search_in, search_for):
        self.search_in = search_in      # The sites we want to search in.
        self.search_for = search_for    # The item we want to search for.

    def data_canada(self):
        for site in self.search_in:    # Only searching for the site selected, instead of searching in all of them.

            if site == 'amazon.ca':    # Run the search on amazon.ca if it was selected.
                try:
                    price_amazon_ca = AmazonCA(self.search_for)    # Initialize the AmazonCA class with the correct search URL.
                    data_amazon_ca = price_amazon_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_amazon_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')
        
                if data_amazon_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    with open("amazon_ca.json", "w") as writeJSON:
                        json.dump(data_amazon_ca, writeJSON, ensure_ascii=False, indent=4)

            if site == 'canadacomputers.com':    # Run the search on canadacomputers.com if it was selected.
                try:
                    price_cc_ca = CanadaComputersCA(self.search_for)    # Initialize the CanadaComputers class with the correct search URL.
                    data_cc_ca = price_cc_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_cc_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')

                if data_cc_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    with open("canadacomputers_ca.json", "w") as writeJSON:
                        json.dump(data_cc_ca, writeJSON, ensure_ascii=False, indent=4)
            
            if site == 'newegg.ca':    # Run the search on newegg.ca if it was selected.
                try:
                    price_newegg_ca = NeweggCA(self.search_for)    # Initialize the NeweggCA class with the correct search URL.
                    data_newegg_ca = price_newegg_ca.set_product_data()    # Get/store the product data by call the set_product_data() function from inside that class.
                    print(f'Web scraping successful for {site}')
                except:
                    data_newegg_ca = None    # If there was a problem pulling the information, set the variable to None.
                    print(f'An error has occured with {site}')
        
                if data_newegg_ca is not None:    # If we sucessfully pulled the information from the site, we'll store it into JSON files.
                    with open("newegg_ca.json", "w") as writeJSON:
                        json.dump(data_newegg_ca, writeJSON, ensure_ascii=False, indent=4)



def main():

    search_in = ['amazon.ca']   # List of the sites to search in.
    search_for = 'msi 3080'    # Search term that the user wants to search for.

    test_run = ItemDataCA(search_in, search_for)
    test_run.data_canada()

if __name__ == '__main__':
    main()