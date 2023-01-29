import os
import logging
import coloredlogs
from constants import Constants
from logging.handlers import TimedRotatingFileHandler

# Create custom logger
logger = logging.getLogger(__name__)
coloredlogs.install(level=Constants.LOG_LEVEL.value)

if not os.path.exists('./logs'):
    os.mkdir('./logs')
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='./logs/app.log',
    when='d',
    interval=1,
    backupCount=30
)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
