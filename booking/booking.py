from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable # pip install prettytable
import csv

class Booking(webdriver.Chrome): # we can use webdriver methods
    def __init__(self,teardown=False):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"

        self.teardown = teardown
        options = Options()
        options.headless = True
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        service = Service(const.PATH)
        
        super(Booking, self).__init__(
            service=service,
            options=options
            )
        
        self.implicitly_wait(5)
        self.maximize_window()
        print("Hello there, This is a booking.com bot")

    def __exit__(self,exc_type, exc_val,exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            accept_cookies = self.find_element(By.ID,'onetrust-accept-btn-handler')
            accept_cookies.click()
        except:
            pass

    def change_currency(self,currency="USD"):
        currency_element = self.find_element(
            By.CSS_SELECTOR,
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        while True:
            try:                
                selected_currency_element = self.find_element(
                By.CSS_SELECTOR,
                f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
                    )
                selected_currency_element.click()
            except NoSuchElementException:
                print("There isn`t this currency, check speling and try again: ")
                currency = input("Select your currency: GEL,EUR,USD,GBP ... ").upper()
            else:
                break


    def select_place_to_go(self,place_to_go):
        search_field = self.find_element(By.ID,'ss')
        search_field.clear() # clear excisting text
        search_field.send_keys(place_to_go)
        first_result = self.find_element(
            By.CSS_SELECTOR,
            'li[data-i="0"]'
            )
        first_result.click()

    def select_dates(self,check_in_date, check_out_date):
        check_in_date = self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date="{check_in_date}"]'
            ) # 2022-05-06
        check_in_date.click()
        check_out_date = self.find_element(
            By.CSS_SELECTOR,
            f'td[data-date="{check_out_date}"]'
            ) # 2022-05-06
        check_out_date.click() # if i need a big range of time, i should add click pages in dates

    def select_adults(self, count=1):
        selection_element = self.find_element(
            By.ID,
            'xp__guests__toggle'
            )
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(
                By.CSS_SELECTOR,
                'button[aria-label="Decrease number of Adults"]'
                )
            decrease_adults_element.click()
            # if the value of adults reaches1, then we should get 
            # out of the while loop
            adults_number_element = self.find_element(
                By.ID,'group_adults'
                )
            adults_number = adults_number_element.get_attribute(
                'value'
                ) # should give back the adults count by attr value

            if int(adults_number) ==1:
                break

        increase_adults_element = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
            )
        
        for i in range(count - 1): #because min adult is already 1 
            increase_adults_element.click()
        
        print("Loading...")


    def click_search(self):          
        search_button = self.find_element(
            By.XPATH, '//button[@type="submit"]'
            )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3,4,5)
        self.implicitly_wait(10)
        filtration.sort_price_lowest_first()

    def report_result(self):
        hotel_boxes = self.find_elements(
            By.XPATH,
            "//div[@data-testid='property-card']"
            )

        report = BookingReport(hotel_boxes)
        # create table object with columns
        columns = ['Hotel Name','Hotel Price','Hotel Score','Hotel Link']
        table = PrettyTable(
            field_names=columns
        ) 
        # add data rows in the table
        table.add_rows(report.pull_deal_box_attributes())

        # with open("hotel_lists.csv", "w") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(columns)
            
        # for row in report.pull_deal_box_attributes():
        #     with open("hotel_lists.csv", 'a') as f:
        #         writer = csv.writer(f)
        #         writer.writerow(row)
        f = open("../hotel_list.csv",'w')
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(report.pull_deal_box_attributes())
        f.close()
        print(table)