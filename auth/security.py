import hashlib
import secrets
import time
from typing import Optional, Tuple
from config import PASSWORD_HASH_ALGORITHM

class SecurityManager:
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """哈希密码，返回(哈希值, 盐)"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        hasher = hashlib.new(PASSWORD_HASH_ALGORITHM)
        hasher.update(f"{password}{salt}".encode('utf-8'))
        password_hash = hasher.hexdigest()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """验证密码"""
        test_hash, _ = SecurityManager.hash_password(password, salt)
        return secrets.compare_digest(test_hash, stored_hash)
    
    @staticmethod
    def generate_session_token() -> str:
        """生成会话令牌"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_current_timestamp() -> int:
        """获取当前时间戳"""
        return int(time.time())