import logging.config
import sys

from module_07_logging_part_2.homework.hw4_dict_config.logger_config import dict_config



class LevelFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.file_name = None

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        if record.levelno == logging.DEBUG:
            self.file_name = "calc_debug.log"
        elif record.levelno == logging.ERROR:
            self.file_name = "calc_error.log"
        with open(self.file_name, mode='a') as f:
            f.write(msg)




def get_logger(name):
    # logging.basicConfig(stream=sys.stdout,level=logging.DEBUG, format='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # file_handler = LevelFileHandler()
    # formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # file_handler.setFormatter(formatter)
    # logging.root.addHandler(file_handler)
    logging.config.dictConfig(dict_config)
    return logger

