from uuid import UUID
from logging import getLogger
logger = getLogger(__name__)

def check_is_valid_uuid(string: str) -> bool:
    try:
        UUID(string)
    except Exception as err:
        logger.info(f"При попытке получить логгер - введён некорректный UUID: {string}")
        return False
    
    return True