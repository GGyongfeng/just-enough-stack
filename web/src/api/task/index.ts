/**
 * 任务管理 API
 */
import { apiClient } from "../client";
import type { Task, TaskCreateRequest, TaskUpdateRequest } from "@/types/task";

export const taskApi = {
  /**
   * 创建任务
   */
  createTask: async (data: TaskCreateRequest) => {
    return apiClient.post<{
      success: boolean;
      message: string;
      data: { task: Task };
    }>("/tasks", data);
  },

  /**
   * 获取任务列表（分页）
   */
  getTasks: async (skip: number = 0, limit: number = 100) => {
    return client.get<{
      success: boolean;
      message: string;
      data: { tasks: Task[]; total: number; skip: number; limit: number };
    }>("/tasks", { params: { skip, limit } });
  },

  /**
   * 获取我的任务
   */
  getMyTasks: async () => {
    return client.get<{
      success: boolean;
      message: string;
      data: { tasks: Task[] };
    }>("/tasks/my");
  },

  /**
   * 获取任务详情
   */
  getTask: async (taskId: number) => {
    return client.get<{
      success: boolean;
      message: string;
      data: { task: Task };
    }>(`/tasks/${taskId}`);
  },

  /**
   * 更新任务
   */
  updateTask: async (taskId: number, data: TaskUpdateRequest) => {
    return client.put<{
      success: boolean;
      message: string;
      data: { task: Task };
    }>(`/tasks/${taskId}`, data);
  },

  /**
   * 删除任务
   */
  deleteTask: async (taskId: number) => {
    return client.delete<{
      success: boolean;
      message: string;
      data: {};
    }>(`/tasks/${taskId}`);
  },
};
