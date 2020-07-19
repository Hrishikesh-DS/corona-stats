from selenium import webdriver
import csv
from threading import Thread
import threading
import schedule
import time

class WebScraper(Thread):
    thread_stop = False

    def __init__(self):
        super().__init__()
        print('WebScraper -> init')
        self.scheduler = schedule.Scheduler()

    def scrape_data(self):
        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        print('scrape_data -> started', threading.get_ident())
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


        print("corona data file is being created.... please wait.")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        driver.get('https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/')

        state_district = []
        for skgm_state in driver.find_elements_by_class_name("skgm-states"):

            state = skgm_state.find_element_by_class_name("show-district").text.strip().replace('\n','').lower()

            skgm_tds = skgm_state.find_elements_by_xpath('.//div[contains(@class,"skgm-districts")]/div[@class="skgm-tr"]/child::div[@class="skgm-td"]')

            districts = []
            
            for i in range(0, len(skgm_tds), 5):

                district = skgm_tds[i].get_attribute('innerHTML').strip().replace('\n','').lower()
                case = skgm_tds[i+1].get_attribute('innerHTML').strip().replace('\n','')
                cured = skgm_tds[i+2].get_attribute('innerHTML').strip().replace('\n','')
                active = skgm_tds[i+3].get_attribute('innerHTML').strip().replace('\n','')
                death = skgm_tds[i+4].get_attribute('innerHTML').strip().replace('\n','')

                districts.append([state,district, case, cured, active, death])

            state_district.extend(districts)

        f = open("sample.csv", "w+")
        f.truncate()
        writer = csv.DictWriter(f, fieldnames=['state','district', 'case', 'cured', 'active', 'death'])
        writer.writeheader()
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(state_district)
        f.close()
        driver.close()
        print('scrape_data -> end')

    def run(self):
        print("web_scraper_thread -> started", threading.get_ident())
        self.scheduler.every().day.at("22:30").do(self.scrape_data)
        # self.scheduler.every(1).minutes.do(self.scrape_data)
        # self.scrape_data()
        while not self.thread_stop:
            self.scheduler.run_pending() 
            time.sleep(1)