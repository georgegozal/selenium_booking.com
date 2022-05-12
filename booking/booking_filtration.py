# this file will include a class with instance methods.
# that will be responsible to interact with our website
# after we have some results, to apply filtrations.
#from typing import List # func(my_list:List):
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self,driver:WebDriver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        # try : 
        #     close_button = self.driver.find_element(
        #         By.XPATH,
        #         'div[@aria-label="Close map"]'
        #     )
        #     close_button.click()
        # except NoSuchElementException:
        #     pass


    def apply_star_rating(self,*star_values):
        star_filtration_box = self.driver.find_element(
            By.CSS_SELECTOR,
            'div[data-filters-group="class"]'
            )
        star_child_elements = star_filtration_box.find_elements(
            By.CSS_SELECTOR,
            '*'
            )
        
        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()
                    self.driver.implicitly_wait(2)

    def sort_price_lowest_first(self):
        lowest_price = self.driver.find_element(
            By.XPATH,
            '//li[@data-id="price"]'
            )
        lowest_price.click()