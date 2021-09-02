import logging


def info(msg):
    print(msg)
    logging.info(msg)

def error(msg):
    print(msg)
    logging.error(msg, exc_info=True)