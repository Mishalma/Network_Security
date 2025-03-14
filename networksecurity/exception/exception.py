# Security_Network/networksecurity/exception/exception.py
import sys
from networksecurity.logging.logger import log  # Changed from 'logger' to 'log'


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message))


if __name__ == '__main__':
    try:
        log.info("Entering try block")  # Changed from logger.info to log.info
        a = 1 / 0
        print("This won't print", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys)