import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

def parse_lines(long_string):
    """Parses a long string into a list of trimmed items."""
    lines = long_string.splitlines()
    items = [line.strip() for line in lines if line.strip()]
    return items


class LinkedInParser:
    def __init__(self, user_data_dir='./user_data.nosync'):

        self.options = webdriver.ChromeOptions()

        # adding argument to disable the AutomationControlled flag 
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        # exclude the collection of enable-automation switches 
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # turn-off userAutomationExtension
        self.options.add_experimental_option('useAutomationExtension', False)

        # self.options.add_argument("--headless")
        # self.options.add_argument("--disable-extensions")

        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.options.add_argument("--window-size=1920,1200")
        self.options.add_argument("user-data-dir=selenium") 

        self.options.add_argument(f"--user-data-dir={user_data_dir}")

        # self.driver = webdriver.Chrome(service=self.s, options=self.options)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        
        # changing the property of the navigator value for webdriver to undefined 
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                '''
        })
        
        self._open_linkedin()

    def __del__(self):
        print('Closing browser')
        self.close_driver()

    def close_driver(self):
        self.driver.quit()

    def _open_linkedin(self):
        print('Opening browser')
        self.driver.get("https://www.linkedin.com/")

        title = self.driver.title
        if "LinkedIn: Log In or Sign Up" in title:
            print("Please, Sign in to linkedin.")
            print("Then press Enter here to continue")
            input()

    def sleep(self, min_s=8.4, max_s=62.2):
        sleep_to = random.uniform(min_s, max_s)
        print(f'Pausing for {sleep_to:.1f} s')
        time.sleep(sleep_to)
    
    def parse_profile(self, url):

        print(f'Parsing: {url}')
        self.driver.get(url)
        self.sleep(1.2, 3.4)
        
        name_txt = ''
        short_about_txt = ''
        company_txt = ''
        last_role = ''

        try:
            section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'artdeco-card')]")))

            try:
                name_txt = WebDriverWait(section, 3).until(EC.presence_of_element_located((By.XPATH, ".//h1"))).text
            except Exception as e:
                print('Error parsing name:', e)

            try:
                short_about_txt = WebDriverWait(section, 3).until(EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'text-body-medium')]"))).text
            except Exception as e:
                print('Error parsing short about:', e)

            try:
                company_txt = WebDriverWait(section, 3).until(EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'inline-show-more-text--is-collapsed')]"))).text
            except Exception as e:
                print('Error parsing company:', e)

        except Exception as e:
            print('Error getting personal section:', e)

        
        try:
            section_experience = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//section[.//div[@id='experience']]")))
            try:
                # a case where there are several roles in one company - we take the last one
                last_role = WebDriverWait(section_experience, 1).until(EC.presence_of_element_located((By.XPATH, "//section[.//div[@id='experience']]/div/ul[1]/li[1]/div/div/div/ul/li[1]/div[@data-view-name='profile-component-entity']"))).text
                last_role = last_role.split('\n')[0]

            except Exception as e:

                try:
                    # the case when there is one role in one - we take it
                    last_role = WebDriverWait(section_experience, 2).until(EC.presence_of_element_located((By.XPATH, "//section[.//div[@id='experience']]/div/ul[1]/li[1]"))).text
                    last_role = last_role.split('\n')[0]
                except Exception as e:
                    print('Error parsing positions data', e)
        
        except Exception as e:
            print('Error getting experience section:', e)
        
        return {
            "url": url, 
            "name_txt": name_txt,
            "short_about_txt": short_about_txt,
            "last_role": last_role,
            "company_txt": company_txt
        }


if __name__ == '__main__':

    # specify the names of the csv files
    csv_input_file = "parse_input.txt"
    csv_output_file = "parsed_output.csv"
    
    # geting a list of linkedin people urls
    with open(csv_input_file, "r", encoding="utf-8") as f:
        code = f.read()
    urls = parse_lines(code)
    
    parser = LinkedInParser()

    res = []
    for index, url in enumerate(urls):
        data = parser.parse_profile(url)
        res.append(data)

        if index < len(urls) - 1:
            parser.sleep()

    df = pd.DataFrame(res)
    df.to_csv(csv_output_file)

    print(f'See results file: {csv_output_file}')
