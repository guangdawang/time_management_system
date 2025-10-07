import json
from pathlib import Path
from typing import List, Dict, Any
from config import TASKS_DIR
from .models import Task, TimeBlock

class TaskStorage:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.task_file = TASKS_DIR / f"{user_id}_tasks.json"
        self.timeblock_file = TASKS_DIR / f"{user_id}_timeblocks.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """确保数据文件存在"""
        for file_path in [self.task_file, self.timeblock_file]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def save_task(self, task: Task) -> bool:
        """保存任务"""
        try:
            tasks = self.load_tasks()
            
            # 查找是否已存在该任务
            existing_index = None
            for i, t in enumerate(tasks):
                if t.task_id == task.task_id:
                    existing_index = i
                    break
            
            if existing_index is not None:
                tasks[existing_index] = task
            else:
                tasks.append(task)
            
            self._save_tasks(tasks)
            return True
        except Exception:
            return False
    
    def load_tasks(self) -> List[Task]:
        """加载所有任务"""
        try:
            with open(self.task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        try:
            tasks = self.load_tasks()
            tasks = [task for task in tasks if task.task_id != task_id]
            self._save_tasks(tasks)
            return True
        except Exception:
            return False
    
    def _save_tasks(self, tasks: List[Task]):
        """保存任务列表"""
        with open(self.task_file, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)
    
    def save_timeblock(self, timeblock: TimeBlock) -> bool:
        """保存时间块"""
        try:
            timeblocks = self.load_timeblocks()
            timeblocks.append(timeblock)
            self._save_timeblocks(timeblocks)
            return True
        except Exception:
            return False
    
    def load_timeblocks(self) -> List[TimeBlock]:
        """加载所有时间块"""
        try:
            with open(self.timeblock_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [TimeBlock.from_dict(block_data) for block_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_timeblocks(self, timeblocks: List[TimeBlock]):
        """保存时间块列表"""
        with open(self.timeblock_file, 'w', encoding='utf-8') as f:
            json.dump([block.to_dict() for block in timeblocks], f, ensure_ascii=False, indent=2)