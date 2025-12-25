<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useTaskStore } from "@/stores/task";
import { ElMessageBox } from "element-plus";
import { Plus, Edit, Delete, View } from "@element-plus/icons-vue";
import type { Task } from "@/types/task";
import {
  TaskStatusLabels,
  TaskPriorityLabels,
  TaskStatusColors,
  TaskPriorityColors,
} from "@/types/task";
import TaskForm from "./components/TaskForm.vue";

const router = useRouter();
const taskStore = useTaskStore();

const showCreateDialog = ref(false);
const filterStatus = ref<string>("");
const filterPriority = ref<string>("");

onMounted(() => {
  taskStore.fetchMyTasks();
});

// 过滤后的任务列表
const filteredTasks = computed(() => {
  let result = taskStore.tasks;

  if (filterStatus.value) {
    result = result.filter((task) => task.status === filterStatus.value);
  }

  if (filterPriority.value) {
    result = result.filter((task) => task.priority === filterPriority.value);
  }

  return result;
});

const handleCreate = async (taskData: any) => {
  await taskStore.createTask(taskData);
  showCreateDialog.value = false;
};

const handleView = (task: Task) => {
  router.push(`/tasks/${task.id}`);
};

const handleEdit = (task: Task) => {
  router.push(`/tasks/${task.id}?mode=edit`);
};

const handleDelete = async (task: Task) => {
  try {
    await ElMessageBox.confirm(`确定要删除任务 "${task.title}" 吗？`, "确认删除", {
      confirmButtonText: "删除",
      cancelButtonText: "取消",
      type: "warning",
    });
    await taskStore.deleteTask(task.id);
  } catch {
    // 用户取消
  }
};
</script>

<template>
  <div class="task-list-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>任务管理</h2>
          <el-button type="primary" :icon="Plus" @click="showCreateDialog = true">
            创建任务
          </el-button>
        </div>
      </template>

      <!-- 筛选器 -->
      <div class="filters">
        <el-select v-model="filterStatus" placeholder="筛选状态" clearable>
          <el-option label="待处理" value="pending" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>

        <el-select v-model="filterPriority" placeholder="筛选优先级" clearable>
          <el-option label="低" value="low" />
          <el-option label="中" value="medium" />
          <el-option label="高" value="high" />
        </el-select>
      </div>

      <!-- 任务表格 -->
      <el-table :data="filteredTasks" v-loading="taskStore.loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="TaskStatusColors[row.status]">
              {{ TaskStatusLabels[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="TaskPriorityColors[row.priority]">
              {{ TaskPriorityLabels[row.priority] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="due_date" label="截止日期" width="180">
          <template #default="{ row }">
            {{ row.due_date ? new Date(row.due_date).toLocaleString() : "-" }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :icon="View" @click="handleView(row)"> 查看 </el-button>
            <el-button size="small" :icon="Edit" @click="handleEdit(row)"> 编辑 </el-button>
            <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建任务对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建任务" width="600px">
      <TaskForm @submit="handleCreate" @cancel="showCreateDialog = false" />
    </el-dialog>
  </div>
</template>

<style scoped>
.task-list-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.filters .el-select {
  width: 200px;
}
</style>
