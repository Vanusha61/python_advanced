import logging

class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.getMessage().encode('ascii')
            return True
        except UnicodeEncodeError:
            return False