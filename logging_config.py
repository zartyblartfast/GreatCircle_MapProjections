import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger()
    file_handler = RotatingFileHandler(filename=os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'app.log'), maxBytes=1024*1024*10, backupCount=0)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
