import csv
import os
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def browse_for_csv():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

def extract_domain(url):
    domain = urlparse(url).netloc
    return domain

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")

        if "In order to show you the most relevant results" in driver.page_source:
            print("Encountered relevant results message. Breaking scroll.")
            break
        
        if new_height == last_height:
            more_button_exists = False
            try:
                more_button = driver.find_element(by=By.CLASS_NAME, value="GNJvt.ipz2Oe")
                more_button_exists = True
                more_button.click()
                time.sleep(2)
            except:
                pass
            if last_height == new_height and not more_button_exists:
                break
            
        last_height = new_height

chrome_driver_path = "C:/Users/sudha/Downloads/chromedriver-win64/chromedriver.exe"
os.environ["CHROME_DRIVER_PATH"] = chrome_driver_path

driver = webdriver.Chrome()

domain_file = browse_for_csv()
if not domain_file:
    print("No file selected. Exiting.")
    exit()

with open(domain_file, 'r') as csvfile:
    domain_reader = csv.reader(csvfile)
    domain_names = [row[0] for row in domain_reader]
    driver.get("https://www.google.com")
    input("Press Enter after the page has loaded...")

for domain in domain_names:
    search_url = f"https://www.google.com/search?q=site:{domain}"
    driver.get(search_url)

    scroll_down(driver)

    page_source = driver.page_source

    start_marker = "UWckNb"
    end_marker = "data-ved"

    start_index = page_source.find(start_marker)
    end_index = page_source.find(end_marker, start_index)

    extracted_urls = set()

    while start_index != -1 and end_index != -1:
        text_to_split = page_source[start_index:end_index]

        role_text_start = "href=\""
        split_text = text_to_split.split(role_text_start)

        for item in split_text[1:]:
            extracted_text = item.split("\"")[0].strip()
            if extracted_text.startswith("http"):
                extracted_urls.add(extracted_text)

        start_index = page_source.find(start_marker, end_index)
        end_index = page_source.find(end_marker, start_index)

    domain_name = domain.split('.')[0]
    csv_filename = f"urls_{domain_name}_google.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for url in extracted_urls:
            csv_writer.writerow([url])
    print(f"CSV file '{csv_filename}' has been created with URLs for domain '{domain}'.")

    domains = set()
    for url in extracted_urls:
        domain = extract_domain(url)
        domains.add(domain)
    domain_names_csv_filename = f"domains_{domain_name}_google.csv"
    with open(domain_names_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for domain in domains:
            csv_writer.writerow([domain])
    print(f"CSV file '{domain_names_csv_filename}' has been created with domain names for domain '{domain}'.")

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Read domain names from the CSV file
csv_filename = "domain_names.csv"

with open(csv_filename, "r") as csvfile:
    domain_reader = csv.reader(csvfile)
    for domain_row in domain_reader:
        domain = domain_row[0]
        
        search_url = f"https://www.bing.com/search?q=site:{domain}"
        driver.get(search_url)

        extracted_urls = set()

        # Find the element containing the number of search results
        search_results_element = driver.find_element(By.CLASS_NAME, "sb_count")
        search_results_text = search_results_element.text

        # Extract the numeric part from the text
        search_results_count = int(''.join(filter(str.isdigit, search_results_text)))

        # Print and store the search results count
        print("Number of search results for", domain, ":", search_results_count)

        time.sleep(2)  # Add a delay to allow the page to load

        # Function to extract URLs from page source
        def extract_urls_from_page(page_source):
            urls = []
            start_marker = "<cite>"
            end_marker = "</cite>"
            start_index = page_source.find(start_marker)
            end_index = page_source.find(end_marker, start_index)
            while start_index != -1 and end_index != -1:
                url = page_source[start_index+len(start_marker):end_index]
                if url.startswith("http"):
                    urls.append(url)
                start_index = page_source.find(start_marker, end_index)
                end_index = page_source.find(end_marker, start_index)
            return urls

        # Extract URLs from the first page
        extracted_urls.update(extract_urls_from_page(driver.page_source))

        current_page_number = 2
        max_page_number = 2 if (search_results_count - 10) <= 10 else search_results_count // 10 + 1    # Set the maximum page number you want to navigate to

        try:
            while current_page_number <= max_page_number:
                print(f"Navigating to page {current_page_number}.")
                xpath = f'//a[@aria-label="Page {current_page_number}"]'
                # Wait for the element to be clickable
                next_page_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                # Scroll to the element
                actions = ActionChains(driver)
                actions.move_to_element(next_page_link).perform()
                next_page_link.click()
                time.sleep(2)
                extracted_urls.update(extract_urls_from_page(driver.page_source))
                current_page_number += 1
        except Exception as e:
            print("Error:", str(e))

        domain_name = domain.split('.')[0]  # Extract
        csv_filename = f"urls_{domain_name}_bing.csv"
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for url in extracted_urls:
                writer.writerow([url])
            print(f"Extracted URLs saved to {csv_filename}")
            
        # Extracting domain names from URLs and creating separate CSV file
        domains = set()
        for url in extracted_urls:
            domain = extract_domain(url)
            domains.add(domain)
        domain_names_csv_filename = f"domains_{domain_name}_bing.csv"
        with open(domain_names_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for domain in domains:
                csv_writer.writerow([domain])
        print(f"CSV file '{domain_names_csv_filename}' has been created with domain names for domain '{domain}'.")

# Close the WebDriver
driver.quit()
