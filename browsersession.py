'''
    PROJECT : Price Comparator
    
    FILENAME : browsersession.py

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

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys

# NOTE: Opening different browser sessions:
#from webdriver_manager.firefox import GeckoDriverManager
    #DRIVER = webdriver.Firefox(executable_path=GeckoDriverManager().install())
#from webdriver_manager.microsoft import EdgeChromiumDriverManager
    #DRIVER = webdriver.Edge(EdgeChromiumDriverManager().install()).
#from webdriver_manager.chrome import ChromeDriverManager
    #DRIVER = webdriver.Chrome(ChromeDriverManager().install()).

class WebBrowserSession():
    def __init__(self):
        #self.DRIVER = webdriver.Firefox(executable_path=GeckoDriverManager().install())    # Open a browser session.
        return

    def open_tab(self, url):
        return

    def close_tab(self):
        self.DRIVER.close()

    def close_session(self):
        self.DRIVER.quit()



# NOTE: need a function to start a webdriver session
# NOTE: need a function to end a webdriver session

# NOTE: need to add efficiency to opening a browser
# NOTE: need to add authenticity to the session
# NOTE:
# NOTE:
# NOTE: