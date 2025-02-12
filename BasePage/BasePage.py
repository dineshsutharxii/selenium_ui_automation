import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utility.utility import Utility


class BasePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    log = Utility().custom_logger()

    def click_element(self, element_to_click):
        try:
            self.driver.execute_script("arguments[0].click();", element_to_click)
        except:
            element_to_click.click()

    def get_attribute_value(self, element, attribute):
        try:
            value = element.get_attribute(attribute)
            # self.log.info(f"{attribute} value of {element} is {value}")
        except Exception as e:
            self.log.info(f"Exception while getting attribute value({attribute}) of {element} because of exception : {str(e)}")
        return value

    # def move_slider(self, slider_element, slider_circle, target_value):
    #     min_value, max_value, slider_width = 0, 2000, slider_element.size['width']
    #     relative_position = (target_value - min_value) / (max_value - min_value)
    #     x_offset = int(relative_position * slider_width)
    #     action = ActionChains(self.driver)
    #     try:
    #         action.click_and_hold(slider_circle).move_by_offset(x_offset, 0).release().perform()
    #     except Exception as e:
    #         self.log.info(f"Exception while moving slider to {target_value} because of exception : {str(e)}")

    def move_slider(self, slider_element, slider_circle, target_value):
        current_value = int(self.get_attribute_value(slider_circle, "aria-valuenow"))
        while True:
            if current_value == target_value:
                return current_value
            if current_value < target_value:
                slider_circle.send_keys(Keys.ARROW_RIGHT)
            else:
                slider_circle.send_keys(Keys.ARROW_LEFT)
            current_value = int(self.get_attribute_value(slider_circle, "aria-valuenow"))
        return -1

    def scroll_to_elememt(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            # self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
            self.log.info(f"Page is scrolled to {element.text}")
        except Exception as e:
            self.log.info(f"Exception during page scrolling to {element.text} because of exception : {str(e)}")
        self.wait.until(EC.visibility_of(element))

    def scroll_by_pixel(self, pixel = 10):
        try:
            self.driver.execute_script("window.scrollBy(0," + str(pixel) + ");")
            self.log.info(f"Page is scrolled to {pixel}")
        except Exception as e:
            self.log.info(f"Exception during page scrolling to {pixel} because of exception : {str(e)}")

    def enter_text(self, web_element, value, current_value="820"):
        self.click_element(web_element)
        web_element.send_keys(Keys.ENTER)
        for i in range(len(str(current_value))):
            web_element.send_keys(Keys.BACKSPACE)
        web_element.send_keys(value)
        web_element.send_keys(Keys.ENTER)
