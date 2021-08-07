import logging

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(filename)s - ' \
             '%(funcName)s(%(lineno)d) - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
