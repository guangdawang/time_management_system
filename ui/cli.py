import os
from typing import List, Optional
from datetime import datetime
from core.models import Task
from core.task_manager import TaskManager

class CLIInterface:
    def __init__(self, task_manager: TaskManager, username: str):
        self.manager = task_manager
        self.username = username
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title: str):
        """显示标题"""
        self.clear_screen()
        print(f"=== 时间管理系统 ===")
        print(f"用户: {self.username}")
        print(f"=== {title} ===")
        print()
    
    def display_tasks(self, tasks: List[Task], show_details: bool = False):
        """显示任务列表"""
        if not tasks:
            print("没有任务")
            return
        
        status_icons = {
            "todo": "○",
            "in_progress": "▶",
            "done": "✓",
            "cancelled": "✗"
        }
        
        priority_icons = {
            "low": "↓",
            "medium": "●",
            "high": "↑",
            "urgent": "‼"
        }
        
        for i, task in enumerate(tasks, 1):
            status_icon = status_icons.get(task.status, " ")
            priority_icon = priority_icons.get(task.priority, " ")
            
            print(f"{i:2d}. [{status_icon}] {priority_icon} {task.title}")
            
            if show_details and task.description:
                print(f"     描述: {task.description}")
            if task.due_date:
                print(f"     截止: {task.due_date}")
            if task.estimated_hours > 0:
                print(f"     预估: {task.estimated_hours}h")
            if task.tags:
                print(f"     标签: {', '.join(task.tags)}")
            print()
    
    def show_main_menu(self):
        """显示主菜单"""
        self.display_header("主菜单")
        print("1. 查看所有任务")
        print("2. 添加任务")
        print("3. 编辑任务")
        print("4. 标记任务状态")
        print("5. 删除任务")
        print("6. 查看统计")
        print("7. 退出系统")
        print()
    
    def get_user_choice(self, prompt: str = "请选择操作: ") -> str:
        """获取用户输入"""
        return input(prompt).strip()
    
    def get_task_input(self, existing_task: Optional[Task] = None) -> dict:
        """获取任务输入"""
        title = input("任务标题: ").strip()
        if not title:
            print("标题不能为空!")
            return None
        
        description = input("任务描述 (可选): ").strip() or existing_task.description if existing_task else ""
        
        priority = input("优先级 (low/medium/high/urgent): ").strip().lower()
        if priority not in ["low", "medium", "high", "urgent"]:
            priority = existing_task.priority if existing_task else "medium"
        
        due_date = input("截止日期 (YYYY-MM-DD, 可选): ").strip() or (existing_task.due_date if existing_task else "")
        
        estimated_hours_input = input("预估小时数 (可选): ").strip()
        if estimated_hours_input:
            try:
                estimated_hours = float(estimated_hours_input)
            except ValueError:
                estimated_hours = existing_task.estimated_hours if existing_task else 0.0
        else:
            estimated_hours = existing_task.estimated_hours if existing_task else 0.0
        
        tags_input = input("标签 (逗号分隔, 可选): ").strip()
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(",")]
        else:
            tags = existing_task.tags if existing_task else []
        
        return {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "estimated_hours": estimated_hours,
            "tags": tags
        }
    
    def show_statistics(self):
        """显示统计信息"""
        stats = self.manager.get_task_statistics()
        
        self.display_header("任务统计")
        print(f"总任务数: {stats['total_tasks']}")
        print(f"已完成: {stats['completed_tasks']}")
        print(f"进行中: {stats['in_progress_tasks']}")
        print(f"待办: {stats['todo_tasks']}")
        print(f"完成率: {stats['completion_rate']:.1%}")
        print(f"总预估时间: {stats['total_estimated_hours']:.1f}h")
        print(f"总实际时间: {stats['total_actual_hours']:.1f}h")
        print()
        input("按回车键继续...")