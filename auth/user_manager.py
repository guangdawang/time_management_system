import json
from typing import Optional, Dict, Any
from pathlib import Path
from config import USERS_FILE, SESSION_TIMEOUT_HOURS, MAX_LOGIN_ATTEMPTS
from .security import SecurityManager

class User:
    def __init__(self, username: str, password_hash: str, salt: str, user_id: str):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.user_id = user_id
        self.login_attempts = 0
        self.locked_until = 0
        self.created_at = SecurityManager.get_current_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "user_id": self.user_id,
            "login_attempts": self.login_attempts,
            "locked_until": self.locked_until,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        user = cls(
            username=data["username"],
            password_hash=data["password_hash"],
            salt=data["salt"],
            user_id=data["user_id"]
        )
        user.login_attempts = data.get("login_attempts", 0)
        user.locked_until = data.get("locked_until", 0)
        user.created_at = data.get("created_at", SecurityManager.get_current_timestamp())
        return user

class UserManager:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Dict] = {}
        self._load_users()
    
    def _load_users(self):
        """加载用户数据"""
        if USERS_FILE.exists():
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = {username: User.from_dict(user_data) 
                                for username, user_data in data.items()}
            except (json.JSONDecodeError, KeyError):
                self.users = {}
    
    def _save_users(self):
        """保存用户数据"""
        data = {username: user.to_dict() for username, user in self.users.items()}
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def register(self, username: str, password: str) -> bool:
        """注册新用户"""
        if username in self.users:
            return False
        
        if len(username) < 3 or len(password) < 6:
            return False
        
        password_hash, salt = SecurityManager.hash_password(password)
        user_id = SecurityManager.generate_session_token()[:8]
        
        user = User(username, password_hash, salt, user_id)
        self.users[username] = user
        self._save_users()
        return True
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """用户登录"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        current_time = SecurityManager.get_current_timestamp()
        
        # 检查账户是否被锁定
        if user.locked_until > current_time:
            return None
        
        if SecurityManager.verify_password(password, user.password_hash, user.salt):
            # 登录成功，重置尝试次数
            user.login_attempts = 0
            self._save_users()
            
            # 创建会话
            session_token = SecurityManager.generate_session_token()
            session_data = {
                "username": username,
                "user_id": user.user_id,
                "created_at": current_time
            }
            self.sessions[session_token] = session_data
            return {"token": session_token, "user": user}
        else:
            # 登录失败，增加尝试次数
            user.login_attempts += 1
            if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
                user.locked_until = current_time + 3600  # 锁定1小时
            self._save_users()
            return None
    
    def verify_session(self, session_token: str) -> Optional[User]:
        """验证会话"""
        if session_token not in self.sessions:
            return None
        
        session_data = self.sessions[session_token]
        current_time = SecurityManager.get_current_timestamp()
        
        # 检查会话是否过期
        if current_time - session_data["created_at"] > SESSION_TIMEOUT_HOURS * 3600:
            del self.sessions[session_token]
            return None
        
        username = session_data["username"]
        return self.users.get(username)
    
    def logout(self, session_token: str):
        """用户登出"""
        if session_token in self.sessions:
            del self.sessions[session_token]