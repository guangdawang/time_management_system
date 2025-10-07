from typing import List, Optional, Dict, Any
import uuid
from .models import Task, TimeBlock
from .storage import TaskStorage

class TaskManager:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.storage = TaskStorage(user_id)
    
    def create_task(self, title: str, **kwargs) -> Task:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            user_id=self.user_id,
            title=title,
            **kwargs
        )
        self.storage.save_task(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def list_tasks(self, status: str = None, priority: str = None) -> List[Task]:
        """列出任务，可筛选"""
        tasks = self.storage.load_tasks()
        
        if status:
            tasks = [task for task in tasks if task.status == status]
        if priority:
            tasks = [task for task in tasks if task.priority == priority]
        
        return tasks
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """更新任务"""
        task = self.get_task(task_id)
        if task and task.user_id == self.user_id:
            task.update(**kwargs)
            return self.storage.save_task(task)
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        task = self.get_task(task_id)
        if task and task.user_id == self.user_id:
            return self.storage.delete_task(task_id)
        return False
    
    def create_timeblock(self, task_id: str, start_time: str, end_time: str, **kwargs) -> TimeBlock:
        """创建时间块"""
        block_id = str(uuid.uuid4())
        timeblock = TimeBlock(
            block_id=block_id,
            user_id=self.user_id,
            task_id=task_id,
            start_time=start_time,
            end_time=end_time,
            **kwargs
        )
        self.storage.save_timeblock(timeblock)
        return timeblock
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        tasks = self.storage.load_tasks()
        
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == "done"])
        in_progress_tasks = len([t for t in tasks if t.status == "in_progress"])
        todo_tasks = len([t for t in tasks if t.status == "todo"])
        
        total_estimated_hours = sum(t.estimated_hours for t in tasks)
        total_actual_hours = sum(t.actual_hours for t in tasks)
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "todo_tasks": todo_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "total_estimated_hours": total_estimated_hours,
            "total_actual_hours": total_actual_hours
        }