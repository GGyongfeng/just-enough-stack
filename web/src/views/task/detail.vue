<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useTaskStore } from "@/stores/task";
import { ArrowLeft, Edit } from "@element-plus/icons-vue";
import {
  TaskStatusLabels,
  TaskPriorityLabels,
  TaskStatusColors,
  TaskPriorityColors,
} from "@/types/task";
import TaskForm from "./components/TaskForm.vue";

const route = useRoute();
const router = useRouter();
const taskStore = useTaskStore();

const taskId = computed(() => parseInt(route.params.id as string));
const editMode = ref(route.query.mode === "edit");

onMounted(() => {
  taskStore.fetchTask(taskId.value);
});

const handleUpdate = async (taskData: any) => {
  await taskStore.updateTask(taskId.value, taskData);
  editMode.value = false;
  await taskStore.fetchTask(taskId.value); // 刷新详情
};

const handleBack = () => {
  router.push("/tasks");
};
</script>

<template>
  <div class="task-detail-page">
    <el-page-header @back="handleBack">
      <template #icon>
        <el-icon><ArrowLeft /></el-icon>
      </template>
      <template #content>
        <span class="page-title">任务详情</span>
      </template>
      <template #extra>
        <el-button v-if="!editMode" type="primary" :icon="Edit" @click="editMode = true">
          编辑
        </el-button>
      </template>
    </el-page-header>

    <el-card v-loading="taskStore.loading" class="task-card">
      <!-- 查看模式 -->
      <div v-if="!editMode && taskStore.currentTask" class="task-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务标题" :span="2">
            {{ taskStore.currentTask.title }}
          </el-descriptions-item>

          <el-descriptions-item label="状态">
            <el-tag :type="TaskStatusColors[taskStore.currentTask.status]">
              {{ TaskStatusLabels[taskStore.currentTask.status] }}
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="优先级">
            <el-tag :type="TaskPriorityColors[taskStore.currentTask.priority]">
              {{ TaskPriorityLabels[taskStore.currentTask.priority] }}
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="截止日期">
            {{
              taskStore.currentTask.due_date
                ? new Date(taskStore.currentTask.due_date).toLocaleString()
                : "-"
            }}
          </el-descriptions-item>

          <el-descriptions-item label="创建时间">
            {{ new Date(taskStore.currentTask.created_at).toLocaleString() }}
          </el-descriptions-item>

          <el-descriptions-item label="任务描述" :span="2">
            {{ taskStore.currentTask.description || "无" }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 编辑模式 -->
      <div v-if="editMode && taskStore.currentTask">
        <TaskForm
          :initial-data="taskStore.currentTask"
          @submit="handleUpdate"
          @cancel="editMode = false"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.task-detail-page {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
}

.task-card {
  margin-top: 20px;
}

.task-info {
  padding: 20px;
}
</style>
