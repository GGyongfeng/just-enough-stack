"""任务状态和优先级枚举"""


class TaskStatus:
    """任务状态枚举"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @classmethod
    def all_statuses(cls):
        """获取所有状态"""
        return [cls.PENDING, cls.IN_PROGRESS, cls.COMPLETED, cls.CANCELLED]

    @classmethod
    def get_description(cls, status: str) -> str:
        """获取状态描述"""
        descriptions = {
            cls.PENDING: "待处理",
            cls.IN_PROGRESS: "进行中",
            cls.COMPLETED: "已完成",
            cls.CANCELLED: "已取消",
        }
        return descriptions.get(status, "未知状态")


class TaskPriority:
    """任务优先级枚举"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def all_priorities(cls):
        """获取所有优先级"""
        return [cls.LOW, cls.MEDIUM, cls.HIGH]

    @classmethod
    def get_description(cls, priority: str) -> str:
        """获取优先级描述"""
        descriptions = {
            cls.LOW: "低",
            cls.MEDIUM: "中",
            cls.HIGH: "高",
        }
        return descriptions.get(priority, "未知优先级")
