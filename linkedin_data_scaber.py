import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook
from tkinter import Tk, Button, Label, filedialog
from tkinter.filedialog import askopenfilename


chrome_driver_path = "C:/Users/sudha/Downloads/chromedriver-win64/chromedriver.exe"
os.environ["CHROME_DRIVER_PATH"] = chrome_driver_path

# Function to extract LinkedIn profile URLs from a text file
def extract_profile_urls_from_text(text_file_path):
    profile_urls = []
    with open(text_file_path, 'r') as file:
        for line in file:
            profile_urls.append(line.strip())
    return profile_urls

# Function to extract data from a LinkedIn profile
def extract_data_from_profile(driver, profile_url):
    driver.execute_script("window.open()")
    driver.get(profile_url)
    # Wait for page to load completely (You may need to implement a proper wait mechanism)
    time.sleep(2)
    page_source = driver.page_source
    
    # Extracting name using text splitting
    name_start_index = page_source.find('<h1 class="text-heading-xlarge inline t-24 v-align-middle break-words">')
    if name_start_index != -1:
        name_end_index = page_source.find('</h1>', name_start_index)
        name = page_source[name_start_index:name_end_index].split('>')[-1].strip()
    else:
        name = "Name not found"

     # Extracting description using text splitting
    description_start_index = page_source.find('data-generated-suggestion-target="urn:li:fsu_profileActionDelegate:-')
    if description_start_index != -1:
        description_end_index = page_source.find('</div>', description_start_index)
        description_text = page_source[description_start_index:description_end_index]
        description = description_text.split('>')[-1].strip().split('<')[0]  # Extract text after '>' and before '<'
    else:
        description = "Description not found"
        
    #  Extracing location using text splitting
    location_start_index = page_source.find('<span class="text-body-small inline t-black--light break-words">')
    if location_start_index != -1:
        location_end_index = page_source.find('</span>', location_start_index)
        location_text = page_source[location_start_index:location_end_index]
        location = location_text.split('>')[-1].strip().split('<')[0]
    else:
        location = "Location not found"

    # Extracting current company using text splitting
    current_company_start_index = page_source.find('<span class="t-14 t-normal">')
    if current_company_start_index != -1:
        current_company_end_index = page_source.find('<!----></span>', current_company_start_index)
        current_company_text = page_source[current_company_start_index:current_company_end_index]
        current_company = current_company_text.split('<!---->')[-1].strip().split('<')[0]  # Extract text after '>' and before '<'
    else:
        current_company = "Experience not found"

    # Extracting current position using text splitting
    current_position_start_index = page_source.find('"experience"')
    if current_position_start_index != -1:
        current_position_end_index = page_source.find('<span class="t-14 t-normal">', current_position_start_index)
        current_position_text = page_source[current_position_start_index:current_position_end_index]
        current_position_text1 = current_position_text.split('mr1 t-bold">')[-1].strip().split('<!----></span>')[0]
        current_position = current_position_text1.split('<!---->')[-1].strip().split('<')[0]  # Extract text after '>' and before '<'
    else:
        current_position = "Position not found"

    # Extracting education using text splitting
    education_start_index = page_source.find('"education"')
    if education_start_index != -1:
        education_end_index = page_source.find('class="pvs-entity__caption-wrapper', education_start_index)
        education_text = page_source[education_start_index:education_end_index]
        education_text1 = education_text.split('<span class="t-14 t-normal">')[-1].strip().split('<!----></span>')[0]  # Extract text after '>' and before '<'
        education = education_text1.split('<!---->')[-1].strip().split('<')[0]
        edu_date_start_index = education_end_index
        edu_date_end_index = page_source.find('<!----></span><span', edu_date_start_index)
        edu_date_text = page_source[edu_date_start_index:edu_date_end_index]
        edu_date = edu_date_text.split('<!---->')[-1].strip().split('<')[0]
    else:
        education = "Education not found"
        edu_date = "Education Date not found"
        
    # Extracting about using text splitting
    about_start_index = page_source.find('"about"')
    if about_start_index != -1:
        about_end_index = page_source.find('"experience"', about_start_index)
        about_text = page_source[about_start_index:about_end_index]
        soup = BeautifulSoup(about_text, 'html.parser')
        about_section = soup.find('div', class_='pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center')
        about = about_section.get_text(strip=True)
    else:
        about = "About not found"

    return name, description, location, current_company, current_position, education, edu_date, about

# Function to browse for a text file containing LinkedIn profile URLs
def browse_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = askopenfilename()  # Open file dialog and return selected file path
    return file_path

# Browse for the text file
text_file_path = browse_file()

# Extract LinkedIn profile URLs from the text file
profile_urls = extract_profile_urls_from_text(text_file_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open LinkedIn homepage
driver.get("https://www.linkedin.com/home")

# Provide some time for the user to interact with the browser (if needed)
input("Please interact with the browser and press Enter when ready...")

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Write headers for the data columns
ws.append(["Name", "Description", "Location", "Experience", "Position", "Education", "Education Date", "About"])

# Iterate over each profile URL and extract data
for profile_url in profile_urls:
    print(f"Extracting data for profile: {profile_url}")
    data = extract_data_from_profile(driver, profile_url)
    
    # Write the extracted data to the Excel worksheet
    ws.append(data)

# Save the Excel workbook with a dynamic filename based on the current timestamp
excel_file_path = f"D:/linkedin_profile_data_{time.strftime('%Y%m%d%H%M%S')}.xlsx"
wb.save(excel_file_path)
