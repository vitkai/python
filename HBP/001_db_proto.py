"""
Descr: db module prototype
@author: vitkai
Created: Sun Dec 15 2019 13:05 MSK
"""
import __main__ as main
import logging
from os import path


def logging_setup():
    logger = logging.getLogger(__name__)
    filename = path.splitext(main.__file__)[0] + '.log'
    handler = logging.FileHandler(filename)

    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-' * 10 + '=' * 10 + '-' * 10 + "\n"))

    return logger



# main starts here
if __name__ == "__main__":
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(__file__)
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))


    logger.debug("That's all folks")
    print("\nThat's all folks")
