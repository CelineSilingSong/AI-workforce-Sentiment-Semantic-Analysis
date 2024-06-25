# Please Work 3
import ssl
import certifi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

# specify the ssl certificate context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# specify the path to the ChromeDriver executable
chrome_driver_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Example of adding a headless argument

# Initialize Chrome WebDriver using Service and Options
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

def get_metadata(url, name_tags, property_tags):
    metadata = {}

    try:
        driver.get(url)

        # Wait for the <head> element to be present
        head = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'head')))

        # Process <meta> tags with 'name' attribute
        for name_tag in name_tags:
            try:
                tag = retry_find_element(head, By.CSS_SELECTOR, f'meta[name="{name_tag}"]')
                metadata[name_tag] = tag.get_attribute('content') if tag else 'N/A'
            except NoSuchElementException:
                metadata[name_tag] = 'N/A'
                print(f"Meta tag 'name={name_tag}' not found in {url}")
            except Exception as e:
                metadata[name_tag] = 'N/A'
                print(f"Error finding meta[name={name_tag}] in {url}: {e}")

        # Process <meta> tags with 'property' attribute
        for property_tag in property_tags:
            try:
                tag = retry_find_element(head, By.CSS_SELECTOR, f'meta[property="{property_tag}"]')
                metadata[property_tag] = tag.get_attribute('content') if tag else 'N/A'
            except NoSuchElementException:
                metadata[property_tag] = 'N/A'
                print(f"Meta tag 'property={property_tag}' not found in {url}")
            except Exception as e:
                metadata[property_tag] = 'N/A'
                print(f"Error finding meta[property={property_tag}] in {url}: {e}")

    finally:
        driver.quit()  # Always quit the driver at the end to close the browser

    return metadata

def retry_find_element(driver, by, value, retries=3, delay=2):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((by, value)))
            # Verify the element is still attached to the DOM
            WebDriverWait(driver, 30).until(EC.staleness_of(element))
            element = driver.find_element(by, value)  # Refresh the element reference
            return element
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException caught on attempt {attempt + 1}, retrying...")
            time.sleep(delay)  # Wait before retrying
    raise NoSuchElementException(f"Element not found with {by}='{value}' after {retries} retries")

# Example usage:
url = "https://news.google.com/rss/articles/CBMiemh0dHBzOi8vd3d3LmZvcmJlcy5jb20vc2l0ZXMvbG91aXNjb2x1bWJ1cy8yMDIwLzAxLzA1L2FpLXNwZWNpYWxpc3QtaXMtdGhlLXRvcC1lbWVyZ2luZy1qb2ItaW4tMjAyMC1hY2NvcmRpbmctdG8tbGlua2VkaW4v0gEA?oc=5"
name_tags = ['keywords', 'twitter:card', 'twitter:site', 'twitter:title', 'twitter:description']  # Example list of name tags
property_tags = ['title', 'description', 'og:title', 'og:description', 'og:type', 'og:url', 'og:site_name', 'og:locale', 'article.type', 'article.section', 'article.summary']  # Example list of property tags

metadata = get_metadata(url, name_tags, property_tags)
print(metadata)