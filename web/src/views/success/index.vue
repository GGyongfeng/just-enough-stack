<template>
  <div class="success-page">
    <div class="success-container">
      <div class="success-content">
        <!-- 图标 -->
        <div class="icon-wrapper">
          <el-icon :size="80" :class="iconClass">
            <component :is="iconComponent" />
          </el-icon>
        </div>

        <!-- 标题 -->
        <h1 class="success-title">{{ pageMessage.title }}</h1>

        <!-- 主要消息 -->
        <p class="success-message">{{ pageMessage.message }}</p>

        <!-- 详细信息 -->
        <div
          v-if="pageMessage.details && pageMessage.details.length > 0"
          class="success-details"
        >
          <ul>
            <li v-for="(detail, index) in pageMessage.details" :key="index">
              {{ detail }}
            </li>
          </ul>
        </div>

        <!-- 返回按钮 -->
        <div class="success-actions" v-if="pageMessage.showReturnButton !== false">
          <el-button type="primary" size="large" @click="handleReturn" :icon="ArrowLeft">
            {{ pageMessage.returnText || "返回" }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  CircleCheck,
  WarningFilled,
  CircleCloseFilled,
  InfoFilled,
  ArrowLeft,
} from "@element-plus/icons-vue";
import type { SuccessPageMessage } from "@/types/api";
import { mittBus } from "@/utils/sys";

const route = useRoute();
const router = useRouter();

// 默认消息
const defaultMessage: SuccessPageMessage = {
  type: "success",
  title: "操作成功",
  message: "您的操作已成功完成",
  showReturnButton: true,
  returnPath: "/",
  returnText: "返回首页",
};

// 页面消息
const pageMessage = computed(
  (): SuccessPageMessage => {
    try {
      const messageParam = route.query.message as string;
      if (messageParam) {
        const decoded = decodeURIComponent(messageParam);
        const parsed = JSON.parse(decoded) as SuccessPageMessage;
        return { ...defaultMessage, ...parsed };
      }
    } catch (error) {
      console.error("解析页面消息失败:", error);
    }
    return defaultMessage;
  }
);

// 图标组件
const iconComponent = computed(() => {
  switch (pageMessage.value.type) {
    case "success":
      return CircleCheck;
    case "warning":
      return WarningFilled;
    case "error":
      return CircleCloseFilled;
    case "info":
    default:
      return InfoFilled;
  }
});

// 图标样式类
const iconClass = computed(() => {
  switch (pageMessage.value.type) {
    case "success":
      return "success-icon";
    case "warning":
      return "warning-icon";
    case "error":
      return "error-icon";
    case "info":
    default:
      return "info-icon";
  }
});

// 处理返回
const handleReturn = () => {
  const returnPath = pageMessage.value.returnPath || "/";
  router.push(returnPath);
};

// 组件挂载时的处理
onMounted(() => {
  // 可以在这里添加一些统计或日志记录
  console.log("成功页面加载:", pageMessage.value);

  // 如果是成功类型的消息，自动触发烟花效果
  if (pageMessage.value.type === "success") {
    setTimeout(() => {
      mittBus.emit("triggerFireworks");
    }, 500); // 延迟500ms让页面先渲染完成
  }
});
</script>

<style scoped>
.success-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(
    135deg,
    var(--el-color-primary-light) 0%,
    var(--el-color-primary-light) 100%
  );
  padding: 20px;
}

.success-container {
  background: var(--el-bg-color);
  border-radius: 20px;
  overflow: hidden;
  max-width: 600px;
  width: 100%;
}

.success-content {
  padding: 60px 40px;
  text-align: center;
}

.icon-wrapper {
  margin-bottom: 30px;
}

.success-icon {
  color: var(--el-color-success);
}

.warning-icon {
  color: var(--el-color-warning);
}

.error-icon {
  color: var(--el-color-danger);
}

.info-icon {
  color: var(--el-color-primary-light);
}

.success-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 20px 0;
  color: var(--el-text-color-primary);
}

.success-message {
  font-size: 18px;
  color: var(--el-text-color-regular);
  margin: 0 0 30px 0;
  line-height: 1.6;
}

.success-details {
  border-radius: 12px;
  padding: 20px;
  margin: 30px 0;
  text-align: left;
}

.success-details ul {
  margin: 0;
  padding-left: 20px;
  color: var(--el-text-color-regular);
  line-height: 1.8;
}

.success-details li {
  margin-bottom: 8px;
}

.success-actions {
  margin-top: 40px;
}

.success-actions .el-button {
  padding: 15px 40px;
  font-size: 16px;
  border-radius: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .success-page {
    padding: 10px;
  }

  .success-content {
    padding: 40px 20px;
  }

  .success-title {
    font-size: 24px;
  }

  .success-message {
    font-size: 16px;
  }

  .icon-wrapper :deep(.el-icon) {
    font-size: 60px !important;
  }
}

/* 动画效果 */
.success-content {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
