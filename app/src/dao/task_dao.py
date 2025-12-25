"""任务数据访问对象"""

from typing import Optional, List
from sqlalchemy.orm import Session
from loguru import logger

from src.dao.base import BaseDAO
from src.orm import TaskModel


class TaskDAO(BaseDAO):
    """任务数据访问对象"""

    def __init__(self, session: Session):
        super().__init__(session, TaskModel)

    def create_task(
        self,
        title: str,
        creator_id: int,
        description: Optional[str] = None,
        status: str = "pending",
        priority: str = "medium",
        due_date: Optional[str] = None,
    ) -> TaskModel:
        """创建任务"""
        task_data = {
            "title": title,
            "creator_id": creator_id,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
        }
        self.add_line(**task_data)
        logger.info(f"Task created: {title}")
        return (
            self._session.query(TaskModel)
            .filter(TaskModel.title == title, TaskModel.creator_id == creator_id)
            .order_by(TaskModel.id.desc())
            .first()
        )

    def get_task_by_id(self, task_id: int) -> Optional[TaskModel]:
        """根据ID获取任务"""
        return self.get_line_by_id(task_id)

    def get_tasks_by_creator(self, creator_id: int) -> List[TaskModel]:
        """获取用户创建的所有任务"""
        return self._session.query(TaskModel).filter(TaskModel.creator_id == creator_id).all()

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[TaskModel]:
        """获取所有任务（分页）"""
        return self._session.query(TaskModel).offset(skip).limit(limit).all()

    def update_task(self, task_id: int, **update_data) -> bool:
        """更新任务"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        for key, value in update_data.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)

        self._session.commit()
        logger.info(f"Task updated: {task_id}")
        return True

    def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self._session.delete(task)
        self._session.commit()
        logger.info(f"Task deleted: {task_id}")
        return True
