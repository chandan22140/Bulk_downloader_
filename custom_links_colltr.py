from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json
import time
import fitz
from selenium.webdriver.chrome.service import Service


def extract_links_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    link_list = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        links = page.get_links()
        for link in links:
            actual_link = link.get('uri')
            if (actual_link) and (actual_link not in link_list) and ("hackerrank.com" in actual_link):
                link_list.append(actual_link)

    pdf_document.close()

    return list(reversed(link_list))

# chrome_driver_path = "chromedriver_64.exe"  # Replace with the path to your chromedriver executable
# chrome_service = ChromeService(chrome_driver_path)
# chrome_options = ChromeOptions()

# Launch Chrome browser


# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
pdf_path = "PDF.pdf"  # Replace with the path to your PDF file
urls_to_scrape = extract_links_from_pdf(pdf_path)
final_urls_to_scrape = {}

# for url in urls_to_scrape:
#     # class_name = url
#     class_link = url
#     print(f"Initializing {url} Download")

#     # Open the URL in the Chrome browser
#     driver.get(class_link)
#     if url == urls_to_scrape[0]:
#         time_sleep(20)
#     else:
#         time_sleep(10)

#     scroll_to_bottom()

#     try:
#         class_name = "__cc_ay_sec__"+name_cleaner(driver.find_element(By.CLASS_NAME, "A6dC2c-J3yWx").text)
#     except:
#         class_name = "__cc_ay_sec__"+name_cleaner(driver.find_element(By.CLASS_NAME, "z3vRcc-J3yWx").text)

#     final_urls_to_scrape[class_name] = class_link


with open(f"link_collection.json", 'w') as f1:
    json.dump(urls_to_scrape, f1, indent=4)
