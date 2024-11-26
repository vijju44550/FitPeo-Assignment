from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class HomePage:

    """
    Page Object for Home page.
    Contains methods to interact with elements on Home page.
    """

    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    # Locators for elements on Home Page
    revenue_calculator_locator = (By.XPATH, "//div[text() = 'Revenue Calculator']/parent::a")

    def click_revenue_calculator(self):

        """ Method used to click on Revenue Calculator link"""

        try:
            # Click on Revenue Calculator link
            self.driver.find_element(*HomePage.revenue_calculator_locator).click()

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

        except ElementNotInteractableException as e:
            # Catch any NoSuchElementException exceptions and print them
            print("Element is not clickable:", e)

        except Exception as e:
            # Catch any unexpected exceptions and print them
            print(f"An error occurred while clicking on Revenue Calculator CTA: {e}")
