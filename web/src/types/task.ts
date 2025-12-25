/**
 * 任务相关类型定义
 */

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  due_date?: string;
  creator_id?: number;
  created_at: string;
  updated_at?: string;
}

export type TaskStatus = "pending" | "in_progress" | "completed" | "cancelled";
export type TaskPriority = "low" | "medium" | "high";

export interface TaskCreateRequest {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

export const TaskStatusLabels: Record<TaskStatus, string> = {
  pending: "待处理",
  in_progress: "进行中",
  completed: "已完成",
  cancelled: "已取消",
};

export const TaskPriorityLabels: Record<TaskPriority, string> = {
  low: "低",
  medium: "中",
  high: "高",
};

export const TaskStatusColors: Record<TaskStatus, string> = {
  pending: "info",
  in_progress: "warning",
  completed: "success",
  cancelled: "danger",
};

export const TaskPriorityColors: Record<TaskPriority, string> = {
  low: "info",
  medium: "warning",
  high: "danger",
};
