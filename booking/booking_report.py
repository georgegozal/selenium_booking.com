# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

class BookingReport:
    def __init__(self,boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element


    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.boxes_section_element:
            # Pullling the hotel name
            hotel_name = deal_box.find_element(
                By.XPATH,
                "./div/div[2]//h3/a/div[1]"
                ).get_attribute("innerHTML").strip().replace("amp;","")
            # print(hotel_name)#.text)
            
            currency = re.match(r"[^&nbsp; 0-9]+",
                                deal_box.find_element(
                                    By.XPATH,
                                    './/div[@ data-testid="price-and-discounted-price"]/span'
                                ).get_attribute("innerHTML")
                                ).group()

            try:
                hotel_price = deal_box.find_element(
                    By.XPATH,
                    './/div[@ data-testid="price-and-discounted-price"]/span[2]'
                    ).get_attribute("innerHTML")

                hotel_price_int = int(re.sub(r"[^0-9]","",hotel_price))
            except NoSuchElementException:
                hotel_price = deal_box.find_element(
                    By.XPATH,
                    './/div[@ data-testid="price-and-discounted-price"]/span'
                    ).get_attribute("innerHTML")

                hotel_price_int = int(re.sub(r"[^0-9]","",hotel_price))
            try:
                hotel_score = deal_box.find_element(
                    By.XPATH,
                    './/div[@data-testid="review-score"]/div'
                    ).get_attribute('innerHTML').strip()
            except NoSuchElementException:
                hotel_score = None

            hotel_link = deal_box.find_element(
                By.CSS_SELECTOR, 
                "a"
                ).get_attribute('href').strip().split('?')[0]

            collection.append(
                [hotel_name,hotel_price_int,hotel_score,hotel_link]
            )
            # print(collection[-1],'\n\n')
        return collection, currency
