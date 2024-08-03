import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# Load the JSON file containing the cookies
with open('kwrojjqm@ellamail.com.json') as f:
    data = json.load(f)

# Extract the cookies
cookies = data['cookie']

# Parse the cookie string into a dictionary
cookies_list = [{'name': cookie.split('=')[0], 'value': cookie.split('=')[1]} for cookie in cookies.split('; ')]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Initialize the WebDriver (make sure to replace 'chromedriver' with the correct path to your ChromeDriver)
service = Service('chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open TikTok
driver.get("https://www.tiktok.com/")

# Add cookies to the browser
for cookie in cookies_list:
    driver.add_cookie(cookie)

# Refresh the page to apply cookies
driver.refresh()

# Wait for the page to load
time.sleep(5)

# Locate the "Edit Profile" button and click it
try:
    edit_profile_button = driver.find_element(By.XPATH, "//span[text()='Изменить профиль']")
    ActionChains(driver).move_to_element(edit_profile_button).click().perform()
    print("Clicked on 'Edit Profile' button.")
except Exception as e:
    print("Failed to find or click 'Edit Profile' button:", e)

# Wait for a while to observe the result
time.sleep(10)

# Close the browser
driver.quit()
