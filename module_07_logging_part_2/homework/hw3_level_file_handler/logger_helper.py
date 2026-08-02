import logging.config
import sys

from module_07_logging_part_2.homework.hw4_dict_config.logger_config import dict_config



class LevelFileHandler(logging.Handler):
    def __init__(self, base_name: str = "log"):
        super().__init__()
        self.base_name = base_name

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        lvl = record.levelname.lower()
        file_name = f"{self.base_name}_{lvl}.log"
        with open(file_name, "w") as f:
            f.write(msg + "\n")



def get_logger(name):
    # logging.basicConfig(stream=sys.stdout,level=logging.DEBUG, format='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # file_handler = LevelFileHandler()
    # formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # file_handler.setFormatter(formatter)
    # logging.root.addHandler(file_handler)
    logging.config.dictConfig(dict_config)
    return logger

