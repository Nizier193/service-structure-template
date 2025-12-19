# Сервис для работы с паролями

import logging
import bcrypt

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.salt_rounds = 12
    
    def hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=self.salt_rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        logger.debug(f"Password hashed successfully")
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        
        is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
        
        logger.debug(f"Password verification: {'success' if is_valid else 'failed'}")
        return is_valid
