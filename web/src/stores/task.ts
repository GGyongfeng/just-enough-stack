/**
 * 任务状态管理
 */
import { defineStore } from "pinia";
import { ref } from "vue";
import { taskApi } from "@/api/task";
import type { Task } from "@/types/task";
import { ElMessage } from "element-plus";

export const useTaskStore = defineStore("task", () => {
  const tasks = ref<Task[]>([]);
  const currentTask = ref<Task | null>(null);
  const loading = ref(false);

  /**
   * 加载任务列表
   */
  const fetchTasks = async () => {
    loading.value = true;
    try {
      const response = await taskApi.getTasks();
      if (response.data.success) {
        tasks.value = response.data.data.tasks;
      }
    } catch (error) {
      ElMessage.error("加载任务列表失败");
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  /**
   * 加载我的任务
   */
  const fetchMyTasks = async () => {
    loading.value = true;
    try {
      const response = await taskApi.getMyTasks();
      if (response.data.success) {
        tasks.value = response.data.data.tasks;
      }
    } catch (error) {
      ElMessage.error("加载我的任务失败");
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  /**
   * 加载任务详情
   */
  const fetchTask = async (taskId: number) => {
    loading.value = true;
    try {
      const response = await taskApi.getTask(taskId);
      if (response.data.success) {
        currentTask.value = response.data.data.task;
      }
    } catch (error) {
      ElMessage.error("加载任务详情失败");
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  /**
   * 创建任务
   */
  const createTask = async (taskData: any) => {
    loading.value = true;
    try {
      const response = await taskApi.createTask(taskData);
      if (response.data.success) {
        ElMessage.success("任务创建成功");
        await fetchTasks(); // 刷新列表
        return response.data.data.task;
      }
    } catch (error: any) {
      ElMessage.error(error.response?.data?.message || "创建任务失败");
      throw error;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 更新任务
   */
  const updateTask = async (taskId: number, taskData: any) => {
    loading.value = true;
    try {
      const response = await taskApi.updateTask(taskId, taskData);
      if (response.data.success) {
        ElMessage.success("任务更新成功");
        await fetchTasks(); // 刷新列表
        return response.data.data.task;
      }
    } catch (error: any) {
      ElMessage.error(error.response?.data?.message || "更新任务失败");
      throw error;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 删除任务
   */
  const deleteTask = async (taskId: number) => {
    loading.value = true;
    try {
      const response = await taskApi.deleteTask(taskId);
      if (response.data.success) {
        ElMessage.success("任务删除成功");
        await fetchTasks(); // 刷新列表
        return true;
      }
    } catch (error: any) {
      ElMessage.error(error.response?.data?.message || "删除任务失败");
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    tasks,
    currentTask,
    loading,
    fetchTasks,
    fetchMyTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
  };
});
