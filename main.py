#!/usr/bin/env python3
"""
时间管理系统 - 主程序入口
"""

import sys
import os

# 添加当前目录到Python路径，确保打包后能正确导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth.user_manager import UserManager

def main():
    user_manager = UserManager()
    current_user = None
    current_session = None
    
    print("=== 时间管理系统 ===")
    
    while True:
        if current_user is None:
            # 未登录状态
            print("\n1. 登录")
            print("2. 注册")
            print("3. 退出")
            
            choice = input("请选择: ").strip()
            
            if choice == "1":
                username = input("用户名: ").strip()
                password = input("密码: ")
                
                result = user_manager.login(username, password)
                if result:
                    current_session = result["token"]
                    current_user = result["user"]
                    print(f"登录成功! 欢迎 {username}")
                else:
                    print("登录失败! 用户名或密码错误，或账户被锁定。")
            
            elif choice == "2":
                username = input("用户名 (至少3字符): ").strip()
                password = input("密码 (至少6字符): ")
                
                if user_manager.register(username, password):
                    print("注册成功! 请登录。")
                else:
                    print("注册失败! 用户名已存在或不符合要求。")
            
            elif choice == "3":
                print("再见!")
                sys.exit(0)
            
            else:
                print("无效选择!")
        
        else:
            # 已登录状态 - 延迟导入以避免循环依赖
            from core.task_manager import TaskManager
            from ui.cli import CLIInterface
            
            task_manager = TaskManager(current_user.user_id)
            cli = CLIInterface(task_manager, current_user.username)
            
            while True:
                cli.show_main_menu()
                choice = cli.get_user_choice()
                
                if choice == "1":
                    # 查看所有任务
                    tasks = task_manager.list_tasks()
                    cli.display_header("所有任务")
                    cli.display_tasks(tasks, show_details=True)
                    input("按回车键继续...")
                
                elif choice == "2":
                    # 添加任务
                    cli.display_header("添加任务")
                    task_data = cli.get_task_input()
                    if task_data:
                        task = task_manager.create_task(**task_data)
                        print(f"任务 '{task.title}' 已创建!")
                    input("按回车键继续...")
                
                elif choice == "3":
                    # 编辑任务
                    tasks = task_manager.list_tasks()
                    cli.display_header("编辑任务")
                    cli.display_tasks(tasks)
                    
                    try:
                        task_num = int(cli.get_user_choice("选择要编辑的任务编号: "))
                        if 1 <= task_num <= len(tasks):
                            task = tasks[task_num - 1]
                            cli.display_header(f"编辑任务: {task.title}")
                            task_data = cli.get_task_input(task)
                            if task_data:
                                if task_manager.update_task(task.task_id, **task_data):
                                    print("任务更新成功!")
                                else:
                                    print("更新失败!")
                        else:
                            print("无效的任务编号!")
                    except ValueError:
                        print("请输入有效的数字!")
                    input("按回车键继续...")
                
                elif choice == "4":
                    # 标记任务状态
                    tasks = task_manager.list_tasks()
                    cli.display_header("标记任务状态")
                    cli.display_tasks(tasks)
                    
                    try:
                        task_num = int(cli.get_user_choice("选择任务编号: "))
                        if 1 <= task_num <= len(tasks):
                            task = tasks[task_num - 1]
                            print(f"\n任务: {task.title}")
                            print("1. 标记为待办")
                            print("2. 标记为进行中")
                            print("3. 标记为完成")
                            
                            status_choice = cli.get_user_choice("选择状态: ")
                            status_map = {"1": "todo", "2": "in_progress", "3": "done"}
                            
                            if status_choice in status_map:
                                if task_manager.update_task(task.task_id, status=status_map[status_choice]):
                                    print("状态更新成功!")
                                else:
                                    print("更新失败!")
                            else:
                                print("无效选择!")
                        else:
                            print("无效的任务编号!")
                    except ValueError:
                        print("请输入有效的数字!")
                    input("按回车键继续...")
                
                elif choice == "5":
                    # 删除任务
                    tasks = task_manager.list_tasks()
                    cli.display_header("删除任务")
                    cli.display_tasks(tasks)
                    
                    try:
                        task_num = int(cli.get_user_choice("选择要删除的任务编号: "))
                        if 1 <= task_num <= len(tasks):
                            task = tasks[task_num - 1]
                            confirm = cli.get_user_choice(f"确认删除任务 '{task.title}'? (y/N): ")
                            if confirm.lower() == 'y':
                                if task_manager.delete_task(task.task_id):
                                    print("任务已删除!")
                                else:
                                    print("删除失败!")
                            else:
                                print("取消删除。")
                        else:
                            print("无效的任务编号!")
                    except ValueError:
                        print("请输入有效的数字!")
                    input("按回车键继续...")
                
                elif choice == "6":
                    # 查看统计
                    cli.show_statistics()
                
                elif choice == "7":
                    # 退出
                    user_manager.logout(current_session)
                    current_user = None
                    current_session = None
                    print("已登出!")
                    break
                
                else:
                    print("无效选择!")
                    input("按回车键继续...")

if __name__ == "__main__":
    main()