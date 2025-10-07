# [file name]: build_gui.py
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_gui_executable():
    """将GUI程序打包成EXE文件"""
    
    print("正在检查依赖...")
    try:
        import PySimpleGUI
    except ImportError:
        print("正在安装PySimpleGUI...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySimpleGUI"])
    
    try:
        import PyInstaller
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("开始打包GUI程序...")
    
    # 打包GUI版本
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',  # 无控制台窗口
        '--name=时间管理系统GUI',
        '--add-data=.;.',
        '--hidden-import=auth.user_manager',
        '--hidden-import=auth.security', 
        '--hidden-import=core.models',
        '--hidden-import=core.storage',
        '--hidden-import=core.task_manager',
        '--hidden-import=config',
        'start_gui.py'
    ]
    
    subprocess.check_call(cmd)
    
    print("GUI版本打包完成！")
    print("可执行文件位置: dist/时间管理系统GUI.exe")
    
    # 复制必要的文件
    dist_dir = Path("dist")
    shutil.copy('config.py', dist_dir / 'config.py')
    shutil.copy('gui_main.py', dist_dir / 'gui_main.py')
    
    # 创建GUI启动脚本
    create_gui_launcher(dist_dir)
    
    print("GUI启动脚本已创建!")

def create_gui_launcher(dist_dir):
    """创建GUI启动脚本"""
    
    bat_content = '''@echo off
chcp 65001 > nul
title 时间管理系统 - 图形界面
echo 正在启动时间管理系统图形界面...
cd /d "%~dp0"
时间管理系统GUI.exe
'''
    
    with open('启动图形界面.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    shutil.copy('启动图形界面.bat', dist_dir / '启动图形界面.bat')

if __name__ == "__main__":
    build_gui_executable()