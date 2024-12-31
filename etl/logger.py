import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path



BASE_DIR = Path(__file__).parent.absolute()
log_path = BASE_DIR / 'logger.log'

logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
file_handler = RotatingFileHandler(
    log_path,
    maxBytes=100000,
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(file_handler)
