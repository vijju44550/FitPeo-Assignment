from selenium.common import NoSuchElementException, TimeoutException, JavascriptException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class RevenueCalculatorPage:

    """
        Page Object for Revenue Calculator page.
        Contains methods to interact with elements on Revenue Calculator page.
    """

    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 20)

    # Locators for elements on Home Page
    slider_locator = (By.CSS_SELECTOR, "input[type='range']")
    slider_button_locator = (By.XPATH, "//span[contains(@class,'MuiSlider-thumb')]")
    slider_track_locator = (By.XPATH, "//span[contains(@class,'MuiSlider-root')]")
    text_field_locator = (By.XPATH, "//input[contains(@class,'MuiInputBase-input') and @type = 'number']")
    total_recurring_amount_locator = (By.XPATH, "//p[contains(text(),'Total Recurring Reimbursement')]/p")

    def checkbox_locator(self, checkbox):

        """ Method to dynamically receive the checkbox to check in and to return the checkbox locator. """

        checkbox_locator = (By.XPATH, "//p[contains(text(),'" + checkbox + "')]/parent::div/label/span/input")
        return checkbox_locator

    def scroll_till_slider_visibility(self):

        """ Method to scroll till Slider is getting visible. """

        try:
            # Wait till slider is present to interact
            self.wait.until(expected_conditions.presence_of_element_located(self.slider_locator))
            slider = self.driver.find_element(*RevenueCalculatorPage.slider_locator)
            # Scroll till slider is getting visible and centre aligned using javascript executor
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

        except TimeoutException as e:
            # Catch any TimeoutException exceptions and print them
            print(f"Timed out waiting for element: {e}")

        except JavascriptException as e:
            # Catch any JavaScriptException exceptions and print them
            print("JavaScript error:", e)

    def adjust_slider(self, target_value):

        """ Method to adjust Slider to required value. """

        try:
            slider = self.driver.find_element(*RevenueCalculatorPage.slider_locator)
            slider_button = self.driver.find_element(*RevenueCalculatorPage.slider_button_locator)
            slider_track = self.driver.find_element(*RevenueCalculatorPage.slider_track_locator)

            # Wait until presence of Slider locator
            self.wait.until(expected_conditions.presence_of_element_located(self.slider_locator))

            """
            Calculate distance that need to be offset from current position to reach required value.
            Formula: offset distance = ((target_value - current_position) * slider_track_width) / slider_range
            """
            current_position = int(slider.get_attribute('aria-valuenow'))
            min_value = int(slider.get_attribute('min'))
            max_value = int(slider.get_attribute('max'))
            slider_range = max_value - min_value
            slider_track_width = slider_track.size['width']
            offset_distance = int(((target_value - current_position) * slider_track_width) / slider_range)

            # Use drag and drop action to move slider to the calculated off set distance
            self.action.drag_and_drop_by_offset(slider_button, offset_distance, 0).perform()

            # Fetch the value of slider after drag and drop action
            value_after_offset = int(slider.get_attribute('aria-valuenow'))

            """
            Validate the difference between target value and value after the  off set.
            As slider offsets with step value. 
            We may not achieve the exact target position using drag and drop.
            """

            difference_after_offset = target_value - value_after_offset

            # Move the remaining difference using keys.
            if difference_after_offset > 0:
                for i in range(difference_after_offset):
                    slider.send_keys(Keys.ARROW_RIGHT)

            elif difference_after_offset < 0:
                for i in range(difference_after_offset):
                    slider.send_keys(Keys.ARROW_LEFT)

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

        except TimeoutException as e:
            # Catch any TimeoutException exceptions and print them
            print(f"Timed out waiting for element: {e}")

    def enter_value_in_text_field(self, target_value):

        """ Method to enter required value in text field. """

        try:
            text_field = self.driver.find_element(*RevenueCalculatorPage.text_field_locator)
            text_field.send_keys(Keys.CONTROL + "a")  # Select already existing value in text field
            text_field.send_keys(str(target_value))  # Replace the existing value with target value

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

    def assert_slider_value(self, target_value):

        """ Method to compare the actual slider position with expected slider value. """

        slider = self.driver.find_element(*RevenueCalculatorPage.slider_locator)

        # Fetch the slider value from UI and store it actual_value variable
        actual_value = int(slider.get_attribute('aria-valuenow'))

        try:
            assert actual_value == target_value  # Assert to compare

        except AssertionError as e:
            # Catch any Assertion error and print them
            assert False, f"An error occurred as slider expected to located at {target_value} but it is located at {actual_value} {e}"

    def assert_text_field_value(self, target_value):

        """ Method to compare the text displayed on UI with expected value. """

        text_field = self.driver.find_element(*RevenueCalculatorPage.text_field_locator)

        # Fetch the value displayed in text field from UI and store it actual_value variable
        actual_value = int(text_field.get_attribute('value'))

        try:
            assert actual_value == target_value  # Assert to compare

        except AssertionError as e:
            # Catch any Assertion error and print them
            assert False, f"An error occurred as text field expected to be displayed as {target_value} but it is displaying {actual_value} {e}"

    def select_checkbox(self, checkbox):

        """ Method to select the checkbox. """

        try:
            checkbox_locator = self.checkbox_locator(checkbox)
            self.driver.find_element(*checkbox_locator).click()  # Select the checkbox

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

    def fetch_total_recurring_amount(self):

        """
        Method to fetch the 'Total Recurring Reimbursement for all Patients Per Month:'
        displayed in header from UI and store it actual_recurring_amount variable.
        And return thr recurring amount
        """

        try:
            total_recurring_amount = self.driver.find_element(*RevenueCalculatorPage.total_recurring_amount_locator).text
            return total_recurring_amount

        except NoSuchElementException as e:
            # Catch any NoSuchElementException exceptions and print them
            print(f"Element not found: {e}")

    def assert_total_recurring_amount(self, expected_recurring_amount):

        """ Method to compare the total recurring amount displayed on UI with expected value. """

        # Get the recurring amount from fetch_total_recurring_amount()
        actual_recurring_amount = self.fetch_total_recurring_amount()

        try:
            assert actual_recurring_amount == expected_recurring_amount  # Assert to compare

        except AssertionError as e:
            # Catch any Assertion error and print them
            assert False, f"An error occurred as recurring amount expected to be {expected_recurring_amount} but it is displayed as {actual_recurring_amount} {e}"
