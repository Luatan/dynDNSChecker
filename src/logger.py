import os
import logging
from environment import Constants
from logging.handlers import TimedRotatingFileHandler

if not os.path.exists('./logs'):
    os.mkdir('./logs')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='./logs/app.log',
    when='d',
    interval=1,
    backupCount=30
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.getLevelName(Constants.LOG_LEVEL.value))

logger.addHandler(file_handler)
logger.addHandler(console_handler)
