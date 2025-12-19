from core.logger import setup_logging, get_logger
from src.index import index
from core.config import config

setup_logging(
    level=config.LOG_LEVEL
)
logger = get_logger("main")
logger.debug("Starting with configuration:")
for key, value in config.model_dump().items():
    logger.debug(f"{key} = {value}")

index()