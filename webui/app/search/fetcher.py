from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


class Fetcher(object):
    """Fetching Capability using Selenium"""

    search_driver = None

    @staticmethod
    def get_selenium_driver(timeout=10):
        if Fetcher.search_driver is not None:
            return Fetcher.search_driver
        else:
            Fetcher.search_driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.CHROME)
            #driver.set_page_load_timeout(timeout)
            return Fetcher.search_driver

    @staticmethod
    def new_selenium_driver(timeout=10):
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.CHROME)
        #driver.set_page_load_timeout(timeout)
        return driver

    @staticmethod
    def close_selenium_driver(driver):
        if driver:
            try:
                driver.close()
                driver.quit()
            except:
                print('An error occurred while closing the driver')

    @staticmethod
    def selenium(url):
        bad_request = False
        driver = Fetcher.new_selenium_driver()
        html = ''
        #text = ''
        title = ''
        try:
            driver.get(url)
        except:
            print('An error occurred while fetching URL: ' + url)
            bad_request = True
        finally:
            try:
                if not bad_request:
                    html = driver.page_source
                    #text = driver.find_element_by_tag_name('body').text
                    title = driver.title
            except:
                print ('An error occurred while fetching URL: ' + url + ' from Selenium')
            finally:
                if driver:
                    Fetcher.close_selenium_driver(driver)
        return [html.encode('utf8')[:20]]

    @staticmethod
    def plain(url):
        res = urlopen(url)
        html = res.read()
        if res.headers.getparam('charset').lower() != 'utf-8':
            html = html.encode('utf-8')
        #start = html.find('<title>') + 7  # Add length of <title> tag
        #end = html.find('</title>', start)
        #title = html[start:end]
        soup = BeautifulSoup(html, 'html.parser')
        return [html, soup.title.string.encode('utf-8'), soup.text.encode('utf-8')]

    @staticmethod
    def fetch(url):
        result = ['','']
        try:
            result = Fetcher.plain(url)
        except:
            print('An error occurred while fetching URL: ' + url + ' using urllib. Skipping it!')
            #print('An error occurred while fetching URL: ' + url + ' using urllib. Trying Selenium...')
            #result = Fetcher.selenium(url)
        return result