# Web Scraping Tool for Extracting URLs from Search Engines

# Overview

This tool is designed to extract URLs related to specific domains from search engine results pages (SERPs). It utilizes Selenium WebDriver to automate web browsing and extract URLs from Google and Bing search engines.

# Features

Google Search: Extracts URLs from Google search results for a specified domain.
Bing Search: Extracts URLs from Bing search results for a specified domain.
CSV Output: Saves the extracted URLs to CSV files for further analysis.

# Prerequisites
Python 3.x
Chrome WebDriver (chromedriver.exe)
Chrome Browser

# Installation
Install Python from python.org.
Download Chrome WebDriver from chromedriver.chromium.org.

# Install required Python packages using pip:
pip install selenium

# Clone or download the source code from the repository.

Update the chrome_driver_path variable in the code with the path to your Chrome WebDriver.
Prepare a CSV file containing the list of domain names you want to search for.
Run the script extract_urls_from_search_engines.py.

# Follow the instructions provided by the script:

Browse for the CSV file containing domain names.
Wait for the browser to open and load search engine pages.
Press Enter after each page has loaded.
The script will extract URLs and save them to CSV files.

# Notes

Adjust the max_page_number variable in the code to control the maximum number of pages to navigate through in search results.
Customize the script to suit your specific requirements or extend its functionality as needed.
