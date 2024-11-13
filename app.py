import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

# try:
# Go to the page
url = 'https://cidades.ibge.gov.br/brasil/rs/caxias-do-sul/panorama'
driver.get(url)

# Optional: Wait until a specific element is present (implies page is fully loaded)
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'lista__nome'))
# )
time.sleep(5)
page_content = driver.page_source

with open("city_ibge_example.html", "w") as file:
    file.write(page_content)
# Get the page content after all JavaScript is loaded

print(page_content)

# finally:
    # Close the browser
    # driver.quit()