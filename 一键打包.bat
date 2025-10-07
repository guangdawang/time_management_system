@echo off
chcp 65001 > nul
title 打包时间管理系统
echo =======================================
echo           时间管理系统打包工具
echo =======================================
echo.

echo 步骤1: 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境!
    echo 请先安装Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 步骤2: 安装打包依赖...
pip install pyinstaller

echo 步骤3: 开始打包...
python build_windows.py

echo.
echo =======================================
echo   打包完成！请查看 dist 文件夹
echo =======================================
echo.
pause