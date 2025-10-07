import os
import sys
from pathlib import Path

# 判断是否打包环境
if getattr(sys, 'frozen', False):
    # 打包后的路径
    BASE_DIR = Path(sys.executable).parent
else:
    # 开发环境路径
    BASE_DIR = Path(__file__).parent

# 数据文件路径
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
TASKS_DIR = DATA_DIR / "tasks"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
TASKS_DIR.mkdir(exist_ok=True)

# 安全配置
PASSWORD_HASH_ALGORITHM = "sha256"
SESSION_TIMEOUT_HOURS = 24
MAX_LOGIN_ATTEMPTS = 5