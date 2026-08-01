import sys
from utils import string_to_operator

import logging
logger = logging.getLogger(__name__)
def calc(args):
    logger.debug("Start calc")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1", exc_info=True)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2",exc_info=True)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    # calc(sys.argv[1:])
    calc('2+3')
