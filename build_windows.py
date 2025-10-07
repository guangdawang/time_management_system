import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """将Python程序打包成EXE文件"""
    
    print("正在检查PyInstaller...")
    try:
        import PyInstaller
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("开始打包程序...")
    
    # 执行打包 - 使用更简单的命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--name=时间管理系统',
        '--add-data=.;.',  # 添加当前目录所有文件
        '--hidden-import=auth.user_manager',
        '--hidden-import=auth.security', 
        '--hidden-import=core.models',
        '--hidden-import=core.storage',
        '--hidden-import=core.task_manager',
        '--hidden-import=ui.cli',
        '--hidden-import=config',
        'main.py'
    ]
    
    subprocess.check_call(cmd)
    
    print("打包完成！")
    print("可执行文件位置: dist/时间管理系统.exe")
    
    # 创建数据目录
    dist_dir = Path("dist")
    data_dir = dist_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    # 创建启动脚本
    create_launcher(dist_dir)
    
    # 复制必要的文件到dist目录
    shutil.copy('config.py', dist_dir / 'config.py')
    
    print("启动脚本和配置文件已创建!")
    return dist_dir

def create_launcher(dist_dir):
    """创建启动脚本"""
    
    # Windows启动脚本
    bat_content = '''@echo off
chcp 65001 > nul
title 时间管理系统
echo 正在启动时间管理系统...
cd /d "%~dp0"
时间管理系统.exe
pause
'''
    
    with open('启动系统.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    # 复制到dist目录
    shutil.copy('启动系统.bat', dist_dir / '启动系统.bat')
    
    # 创建使用说明
    readme_content = '''时间管理系统 - 使用说明

1. 双击「启动系统.bat」运行程序
2. 首次使用需要注册账户
3. 所有数据保存在 data 文件夹中
4. 如需重新安装，删除整个文件夹即可

功能特点：
- 用户注册登录
- 任务创建、编辑、删除
- 任务优先级和状态管理
- 数据统计和进度跟踪

注意事项：
- 请勿删除 data 文件夹，否则会丢失所有数据
- 建议定期备份重要数据
'''
    
    with open(dist_dir / '使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    build_executable()