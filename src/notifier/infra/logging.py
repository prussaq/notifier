import logging
import os

from ..main import RUN_ID, ROOT_DIR

LOG_DIR = os.path.join(ROOT_DIR, "logs")

initialized = False


def init():
    global initialized
    from .config import configs

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"{RUN_ID}.log")
    
    if os.path.exists(log_path): 
        os.remove(log_path)

    log_level = configs['logging']['level'].upper()
    log_format = '%(asctime)s %(levelname)s %(threadName)s [%(name)s:%(lineno)d] - %(message)s'
    logging.basicConfig(level=log_level, filename=log_path, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    initialized = True