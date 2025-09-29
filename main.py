from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
from datetime import datetime
import time
from tkinter import *


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

window = Tk()
window.geometry("1280x720")
window.title("WebScraper")

frame = Frame(window, padx=20, pady=20)
frame.pack(expand=True)


position_label = Label(frame, text="Position", font=("Arial", 14), anchor="w")
position_label.grid(row=0, column=0, pady=10, sticky="w")
position_entry = Entry(frame, font=("Arial", 14), width=30)
position_entry.grid(row=0, column=1, pady=10)
position_entry.insert(0, "Controller")

radius_label = Label(frame, text="Radius", font=("Arial", 14), anchor="w")
radius_label .grid(row=1, column=0, pady=10, sticky="w")
radius_entry = Entry(frame, font=("Arial", 14), width=30)
radius_entry.grid(row=1, column=1, pady=10)
radius_entry.insert(0, "25")


page_label = Label(frame, text="Page (in increments of 10)", font=("Arial", 14), anchor="w")
page_label.grid(row=2, column=0, pady=10, sticky="w")
page_entry = Entry(frame, font=("Arial", 14), width=30)
page_entry.grid(row=2, column=1, pady=10)
page_entry.insert(0, "")


def scrape_indeed(position, radius, start_value):
    url = f"https://de.indeed.com/Jobs?q={position}&l=Aschaffenburg,+Bayern&radius={radius}&start={start_value}"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    job_column = wait.until(EC.presence_of_element_located((By.ID, 'mosaic-jobResults')))

    job_list = job_column.find_elements(By.CSS_SELECTOR, '[data-testid="slider_item"]')

    print(f"Found {len(job_list)} job listings")


    job_URLs = []
    for i, item in enumerate(job_list):
        try:
            further_link = item.find_element(By.CSS_SELECTOR, 'h2 a')
            job_url = further_link.get_attribute('href')

            if job_url and job_url.startswith('http'):
                    job_URLs.append(job_url)
        except Exception as e:
            print(f"Error getting URL {i + 1}: {e}")
            continue

    jobs_data = []
    for i, job_url in enumerate(job_URLs):
        try:
            print(f"Scraping job {i + 1}/{len(job_URLs)}")

            driver.get(job_url)
            time.sleep(3)

            wait_detail = WebDriverWait(driver, 15)
            description_element = wait_detail.until(
                EC.presence_of_element_located((By.ID, 'jobDescriptionText'))
            )
            job_description = description_element.text

            try:
                title = driver.find_element(By.CSS_SELECTOR, 'h1.jobsearch-JobInfoHeader-title').text
            except:
                title = ""

            try:
                company = driver.find_element(By.CSS_SELECTOR, '[data-testid="inlineHeader-companyName"]').text
            except:
                company = ""

            try:
                location = driver.find_element(By.CSS_SELECTOR, '[data-testid="inlineHeader-companyLocation"]').text
            except:
                location = ""


            print(f"Job {i + 1}: {title}")
            job_data = {'Title': title,
                        'Company': company,
                        'Location': location,
                        'Job_Description': job_description}

            jobs_data.append(job_data)

        except Exception as e:
            print(f"Error processing job {i + 1}: {e}")
            continue

    return jobs_data

def save_to_files(jobs_data):

    if not jobs_data:
        print("No data")
        return

    df = pd.DataFrame(jobs_data)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"indeed_jobs_{timestamp}"

    csv_filename = f"{base_filename}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"Data saved to CSV: {csv_filename}")

    excel_filename = f"{base_filename}.xlsx"
    df.to_excel(excel_filename, index=False, engine='openpyxl')
    print(f"Data saved to Excel: {excel_filename}")

    print(f"Total jobs scraped: {len(jobs_data)}")
    return csv_filename, excel_filename

def handle_submit():
    data = scrape_indeed(
        position_entry.get(),
        radius_entry.get(),
        page_entry.get()
    )

    save_to_files(data)

submit_button = Button(frame, text="Scrape", font=("Arial", 14), width=20, command = handle_submit)
submit_button.grid(row=3, columnspan=2, pady=20)

window.mainloop()