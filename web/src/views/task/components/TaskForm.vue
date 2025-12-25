<script setup lang="ts">
import { ref, reactive } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import type { Task, TaskCreateRequest } from "@/types/task";

interface Props {
  initialData?: Task;
}

const props = defineProps<Props>();
const emit = defineEmits(["submit", "cancel"]);

const formRef = ref<FormInstance>();
const formData = reactive<TaskCreateRequest>({
  title: props.initialData?.title || "",
  description: props.initialData?.description || "",
  status: props.initialData?.status || "pending",
  priority: props.initialData?.priority || "medium",
  due_date: props.initialData?.due_date || undefined,
});

const rules: FormRules = {
  title: [
    { required: true, message: "请输入任务标题", trigger: "blur" },
    { min: 1, max: 200, message: "标题长度在 1 到 200 个字符", trigger: "blur" },
  ],
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate((valid) => {
    if (valid) {
      emit("submit", formData);
    }
  });
};

const handleCancel = () => {
  emit("cancel");
};
</script>

<template>
  <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
    <el-form-item label="任务标题" prop="title">
      <el-input v-model="formData.title" placeholder="请输入任务标题" />
    </el-form-item>

    <el-form-item label="任务描述">
      <el-input
        v-model="formData.description"
        type="textarea"
        :rows="4"
        placeholder="请输入任务描述（可选）"
      />
    </el-form-item>

    <el-form-item label="状态">
      <el-select v-model="formData.status" placeholder="请选择状态">
        <el-option label="待处理" value="pending" />
        <el-option label="进行中" value="in_progress" />
        <el-option label="已完成" value="completed" />
        <el-option label="已取消" value="cancelled" />
      </el-select>
    </el-form-item>

    <el-form-item label="优先级">
      <el-select v-model="formData.priority" placeholder="请选择优先级">
        <el-option label="低" value="low" />
        <el-option label="中" value="medium" />
        <el-option label="高" value="high" />
      </el-select>
    </el-form-item>

    <el-form-item label="截止日期">
      <el-date-picker
        v-model="formData.due_date"
        type="datetime"
        placeholder="选择截止日期（可选）"
        format="YYYY-MM-DD HH:mm:ss"
        value-format="YYYY-MM-DDTHH:mm:ss"
      />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="handleSubmit">
        {{ initialData ? "更新" : "创建" }}
      </el-button>
      <el-button @click="handleCancel">取消</el-button>
    </el-form-item>
  </el-form>
</template>
