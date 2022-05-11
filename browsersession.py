# Noah Arcand Da Silva
# 2021-03-07 (YYYY-MM-DD)
# Price Comparator - websession.py
# Version 1.0

""" NOTE — ABOUT THIS PROGRAM 
...
"""

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