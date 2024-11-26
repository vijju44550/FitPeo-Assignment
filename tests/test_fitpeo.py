from page_objects.home_page import HomePage
from page_objects.revenue_calculator_page import RevenueCalculatorPage
from utilities.base_class import BaseClass


class TestFitpeo(BaseClass):

    """ Class to store Test methods. """

    def test_recurring_amount_validation(self):

        """ Method to test Total Recurring Reimbursement for all Patients Per Month. """

        # Store the get_logger method from BaseClass in log variable
        log = self.get_logger()

        # Required data
        slider_target_value = 820
        textField_target_value = 560
        expected_recurring_amount = '$110700'
        checkbox1 = 'CPT-99091'
        checkbox2 = 'CPT-99453'
        checkbox3 = 'CPT-99454'
        checkbox4 = 'CPT-99474'

        # Store page objects in variables
        homepage = HomePage(self.driver)
        revenue_calculator_page = RevenueCalculatorPage(self.driver)

        homepage.click_revenue_calculator()  # Call method to click on Revenue Calculator link.
        revenue_calculator_page.scroll_till_slider_visibility()  # Call method to scroll till slider is visible.
        log.info("Clicked on Revenue Calculator link")

        # Call method to adjust slider till required position i.e., slider_target_value.
        revenue_calculator_page.adjust_slider(slider_target_value)

        # Call method to compare actual slider position with expected slider position.
        revenue_calculator_page.assert_slider_value(slider_target_value)
        # Call method to compare actual value displayed in text field with expected value.
        revenue_calculator_page.assert_text_field_value(slider_target_value)

        log.info("Target value is adjusted on Slider")

        # Call method to enter the value in text field with expected value.
        revenue_calculator_page.enter_value_in_text_field(textField_target_value)

        # Call method to compare actual value displayed in text field with expected value.
        revenue_calculator_page.assert_text_field_value(textField_target_value)

        # Call method to compare actual slider position with expected slider position.
        revenue_calculator_page.assert_slider_value(textField_target_value)

        log.info("Required value is entered in text field")

        # Call method to enter the value in text field with slider_target_value i.e., 820 as final amount to validate is referring with 820.
        revenue_calculator_page.enter_value_in_text_field(slider_target_value)
        
        # Call method to select the checkbox
        revenue_calculator_page.select_checkbox(checkbox1)
        revenue_calculator_page.select_checkbox(checkbox2)
        revenue_calculator_page.select_checkbox(checkbox3)
        revenue_calculator_page.select_checkbox(checkbox4)

        log.info("Selected required checkboxes")

        print("{} {}".format("Total Recurring Reimbursement for all Patients Per Month:", revenue_calculator_page.fetch_total_recurring_amount()))
        log.info("Total Recurring Reimbursement for all Patients Per Month:" + revenue_calculator_page.fetch_total_recurring_amount())

        revenue_calculator_page.assert_total_recurring_amount(expected_recurring_amount)
