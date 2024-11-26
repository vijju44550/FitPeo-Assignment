import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utilities.base_class import BaseClass
driver = None

base_class = BaseClass  # Initialize the base_class to get the logger
log = base_class.get_logger()  # Store the get_logger method from BaseClass in log variable


def pytest_addoption(parser):

    """ Method to pass command-line option to select the browser at run time """

    try:
        parser.addoption(
            # Command-line option to select the browser at run time
            "--browser_name", action="store", default="chrome"
        )

    except Exception as e:
        # Catch any unexpected exceptions and print them
        print(f"An error occurred while adding command-line options: {e}")


@pytest.fixture(scope="class")
def setup(request):
    """
    Fixture that initializes and closes the browser.
    Setup and teardown of Webdriver  instance for test
    """

    global driver
    log.info("Initializing Browser")
    browser_name = request.config.getoption("--browser_name")

    # Setup: Launch Chrome Browser
    if browser_name == "chrome":
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options_chrome)

    # Setup: Launch Firefox Browser
    elif browser_name == "firefox":
        options_firefox = Options()
        driver = webdriver.Firefox(options=options_firefox)
        driver.maximize_window()

    # Setup: Launch Edge Browser
    elif browser_name == "edge":
        options_edge = webdriver.EdgeOptions()
        options_edge.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options_edge)

    log.info("Hitting the URL")
    driver.get("https://www.fitpeo.com/")  # Hit the URL
    request.cls.driver = driver
    yield  # Test Execution

    # Teardown: Close the browser after test
    log.info("Closing the browser")
    driver.close()
