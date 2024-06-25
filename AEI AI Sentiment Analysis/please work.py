import feedparser
import pandas as pd
from datetime import datetime, timedelta
import ssl
import certifi
import requests
import numpy as np
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException 


# specify the ssl certificate context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# speficy the path to the ChromeDriver executable
chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Example of adding a headless argument

# Initialize Chrome WebDriver using Service and Options
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Path to directory:
directory_path = '/Users/LindaSong/Desktop/AI job 3'

class ElementWrapper:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator
        self.element = None

    def find(self):
        try:
            self.element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element with locator {self.locator} not found.")
        
        except StaleElementReferenceException:
            # If element is stale, re-locate it
            self.element = self.driver.find_element(*self.locator)

    def click(self):
        self.find()  # Ensure element is located
        try:
            self.element.click()
        except StaleElementReferenceException:
            # If element is stale, re-locate it and try again
            self.find()
            self.element.click()

    def get_attribute(self, attribute):
        self.find()  # Ensure element is located
        return self.element.get_attribute(attribute) if self.element else None

def fetch_article_metadata(url):
    # Initialize metadata dictionary
    metadata = {}
    # Tags to extract
    name_tags = ['keywords', 'twitter:card', 'twitter:site', 'twitter:title', 'twitter:description', 'article.type', 'article.section', 'article.summary']
    property_tags = ['title', 'description', 'og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale']

    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # Implicit wait for elements to load
    
    try:
        driver.get(url)

        # Wait for the <head> element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'head')))

        # Switch to the head element
        head = driver.find_element(By.TAG_NAME, 'head')

        for name_tag in name_tags:
            try:
                wrapper = ElementWrapper(head, (By.CSS_SELECTOR, f'meta[name="{name_tag}"]'))
                metadata[name_tag] = wrapper.get_attribute('content') or 'N/A'
            except NoSuchElementException:
                metadata[name_tag] = 'N/A'
                print(f"Meta tag 'name={name_tag}' not found in {url}")
            except Exception as e:
                metadata[name_tag] = 'N/A'
                print(f"Error finding meta[name={name_tag}] in {url}: {e}")

        for property_tag in property_tags:
            try:
                wrapper = ElementWrapper(head, (By.CSS_SELECTOR, f'meta[property="{property_tag}"]'))
                metadata[property_tag] = wrapper.get_attribute('content') or 'N/A'
            except NoSuchElementException:
                metadata[property_tag] = 'N/A'
                print(f"Meta tag 'property={property_tag}' not found in {url}")
            except Exception as e:
                metadata[property_tag] = 'N/A'
                print(f"Error finding meta[property={property_tag}] in {url}: {e}")

        return metadata

    except TimeoutException as te:
        print(f"Timeout while fetching URL: {te}")
        return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None
    finally:
        driver.quit()
            

def main():
    files = os.listdir(directory_path)

    for file in files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)
        
        all_metadata = []

        for index, row in df.iterrows():
            url = row[0]

            delay = random.uniform(1, 3)  # Random delay between 1 to 3 seconds
            time.sleep(delay)

            meta_data = fetch_article_metadata(url)
            if meta_data:
                print(f"Obtained metadata successfully for {url}")
                all_metadata.append(meta_data)
            else:
                print(f"Failed to scrape {url}")

        if all_metadata:
            meta_data_df = pd.DataFrame(all_metadata)
            df = pd.concat([df, meta_data_df], axis=1)
            df.to_csv(f'/Users/LindaSong/Desktop/AI job 5/meta_{file}', index=False)
        else:
            print(f"No metadata collected for {file}")
    
    driver.quit()

if __name__ == "__main__":
    main()