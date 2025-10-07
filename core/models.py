from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
import uuid

@dataclass
class Task:
    task_id: str
    user_id: str
    title: str
    description: str = ""
    created_at: str = None
    updated_at: str = None
    status: str = "todo"  # todo, in_progress, done, cancelled
    priority: str = "medium"  # low, medium, high, urgent
    due_date: Optional[str] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    tags: List[str] = None
    
    def __post_init__(self):
        current_time = datetime.now().isoformat()
        if self.created_at is None:
            self.created_at = current_time
        if self.updated_at is None:
            self.updated_at = current_time
        if self.tags is None:
            self.tags = []
    
    def to_dict(self):
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建实例"""
        return cls(**data)
    
    def update(self, **kwargs):
        """更新任务属性"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def mark_done(self):
        """标记为完成"""
        self.status = "done"
        self.updated_at = datetime.now().isoformat()
    
    def mark_in_progress(self):
        """标记为进行中"""
        self.status = "in_progress"
        self.updated_at = datetime.now().isoformat()

@dataclass
class TimeBlock:
    block_id: str
    user_id: str
    task_id: str
    start_time: str
    end_time: str
    description: str = ""
    actual_hours: float = 0.0
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)