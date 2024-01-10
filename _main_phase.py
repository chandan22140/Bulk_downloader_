from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import TimeoutException

import requests
import os
from _downloader_functions import name_cleaner
import json
from _seconary_phase import do_seconary_phase
import time
import telebot
import traceback
import subprocess


command = "pip install -r _req.txt"
try:
    # subprocess.check_call(command, shell=True)
    print("Requirements installed successfully.")
except subprocess.CalledProcessError:
    print("Error installing requirements.")


API_KEY = "5991202973:AAG8u83Knyd2fDz8x7jJ99UuNa0fKihZWOY"
bot = telebot.TeleBot(API_KEY, parse_mode=None)
err = ""

wait_time = 4
login_time = 15


def time_sleep(t):
    for i in range(t):
        time.sleep(1)
        print(t-i)


def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Set up Chrome WebDriver
# Replace with the path to your chromedriver executable
if not (os.path.exists("final.json")):
    try:
        chrome_driver_path = "_chromedriver_64.exe"
        chrome_service = ChromeService(chrome_driver_path)
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless")  # Uncomment this line if you want to run Chrome in headless mode

        # Launch Chrome browser
        driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)
        # 1-21   2-22
        with open(f"link_collection.json", 'r') as f1:
            urls_to_scrape = json.load(f1)
        data = {

        }

        list_of_urls_to_scrape = list(urls_to_scrape.keys())
        for unique_class_name in list_of_urls_to_scrape:
            if "__cc_ay_sec__" in unique_class_name:
                continue
            classroom_all_links = []
            all_links_found = False
            class_name = unique_class_name
            class_link = urls_to_scrape[unique_class_name]
            print(f"Initializing {class_name} Download")

            # Open the URL in the Chrome browser
            driver.get(class_link)

            if unique_class_name == list_of_urls_to_scrape[0]:
                time_sleep(login_time)
            else:
                time_sleep(wait_time)

            scroll_to_bottom()

            classroom_data = []



            class_name_to_scrape = "xUYklb"  # Replace with the class name you want to scrape
            categories = driver.find_elements(
                By.CLASS_NAME, class_name_to_scrape)

            for cat in categories:
                try:
                    cat_link = cat.get_attribute("href")
                    cat_name = name_cleaner(cat.text)

                    classroom_data.append(
                        {"category_name": cat_name, "category_link": cat_link})

                except:
                    pass

            data[class_name] = {}
            for category in classroom_data:

                data[class_name][category["category_name"]] = {}

                driver.get(category['category_link'])
                time_sleep(wait_time)
                scroll_to_bottom()
                lectures = driver.find_elements(By.CLASS_NAME, "jrhqBd")
                for lecture in lectures:
                    try:
                        lecture_name = name_cleaner(lecture.find_element(
                            By.CLASS_NAME, "ToDHyd").find_element(By.TAG_NAME, "div").text.split(": ")[1])
                        print("lecture name: "+lecture_name)

                        data[class_name][category['category_name']
                                         ][lecture_name] = {}

                        materials = lecture.find_elements(
                            By.CLASS_NAME, "luto0c")

                        for mat in materials:
                            mat_name = mat.find_element(
                                By.CLASS_NAME, "zZN2Lb-Wvd9Cc").text
                            mat_link = mat.find_element(
                                By.TAG_NAME, "a").get_attribute("href")

                            print("mat_name: "+mat_name)
                            print("mat_link: "+mat_link)
                            classroom_all_links.append(mat_link)


                            data[class_name][category['category_name']
                                             ][lecture_name][mat_link] = name_cleaner(mat_name)

                    except:
                        print("no lecture name found")


            # ---------------------------------------Common untitiled scenario---------------------------------------
            driver.get(class_link)
            scroll_to_bottom()
            data[class_name]["Miscellaneous_"] = {}

            # Iterate through each "View more" button and click on it using JavaScript
            view_more_buttons = driver.find_elements(By.CLASS_NAME, "VfPpkd-vQzf8d")
            for view_more_button in view_more_buttons:
                try:
                    if view_more_button.text == "View more":
                        driver.execute_script("arguments[0].scrollIntoView();", view_more_button)
                        driver.execute_script("arguments[0].click();", view_more_button)
                        # view_more_button.click()
                        print("Clicked on the View more button")
                        time_sleep(5)

                except:
                    print("not clickable")
            
            # Iterate through each row item and click on it
            row_collections = driver.find_elements(By.CLASS_NAME, "tfGBod")
            for row in row_collections:
                if all_links_found:
                    break

                driver.execute_script("arguments[0].scrollIntoView(false);", row)
                row.click()

                try:
                    WebDriverWait(row, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "luto0c")))
                    print("File loaded successfully.")
                except TimeoutException:
                    print("Timeout waiting for page to load.")
                
                lecture_name = row.find_element( By.CLASS_NAME, "UzbjTd").text
                print("lecture name: "+lecture_name)
                data[class_name]["Miscellaneous_"][lecture_name] = {}

                materials = row.find_elements( By.CLASS_NAME, "luto0c")
                for mat in materials:
                    mat_link = mat.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if mat_link in classroom_all_links:
                        all_links_found = True
                        break
                    print("mat_link: "+mat_link)
                    data[class_name]["Miscellaneous_"][lecture_name][mat_link] = ""

            # ---------------------------------------Common untitiled scenario---------------------------------------
                    

            with open(f"check.json", 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{class_name} Downloading completed")

        driver.quit()
        with open(f"final.json", 'w') as f:
            json.dump(data, f, indent=4)
        os.remove("check.json")

        print("licsenced by Tharun Harish ")

        bot.send_message(800851598, "classroom_scraper_done!1")

        files = {"document": open("final.json", "rb")}
        resp = requests.post("https://api.telegram.org/bot" +
                             API_KEY + "/sendDocument?chat_id=800851598", files=files)


        if (resp.status_code == 200):
            bot.send_message(800851598, "Sucessfully sent")
        else:
            bot.send_message(800851598, "Bad sent")

    except Exception as e:
        e = traceback.format_exc(limit=None, chain=True)
        traceback.print_exc()

        bot.send_message(
            800851598, f"Phase1_classroom_scraper threw error!!\n```{e}```")
        err = 1

if (err == ""):
    try:
        do_seconary_phase()

    except Exception as e2:
        e2 = traceback.format_exc(limit=None, chain=True)
        bot.send_message(
            800851598, f"Phase2_bulk_download threw error!!\n```{e2}```")
        traceback.print_exc()
