import pytest
import inspect
import logging


@pytest.mark.usefixtures("setup")
class BaseClass:

    """ Class that contains common functionality or setup code shared across multiple test case or page """

    @staticmethod
    def get_logger():

        """ Method that returns a logger instance """

        try:
            logger_name = inspect.stack()[1][3]  # Line to dynamically retrieve the name of the function or method
            logger = logging.getLogger(logger_name)  # Create logger
            file_handler = logging.FileHandler('logfile.log')  # Create file handler
            # Create formatter
            formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)  # Add the handler to the logger
            logger.setLevel(logging.INFO)  # Set log level to INFO
            return logger

        except Exception as e:
            # Catch any unexpected exceptions and print them
            print(f"Unexpected error occurred while calling logger: {e}")
