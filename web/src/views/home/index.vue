<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { UploadFilled, TrendCharts, DataAnalysis, Shop } from "@element-plus/icons-vue";
import { mittBus } from "@/utils/sys";

import { ROUTES } from "@/router/routes";

// 导入图片资源
import bp from "@/assets/img/ceremony/hb.png";

const router = useRouter();

// 烟花系统状态
const timerRef = ref<ReturnType<typeof setInterval> | null>(null);
const isLaunching = ref(false);

const openBili = () => {
  window.open(
    "https://www.bilibili.com/video/BV1uqVFzNET8/?spm_id_from=333.337.search-card.all.click&vd_source=e9ad9a4b36e4ad35f5726252491a9536",
    "_blank"
  );
};

// 烟花触发核心函数
const triggerFireworks = (count: number, src?: string) => {
  // 清除之前的定时器
  if (timerRef.value) {
    clearInterval(timerRef.value);
    timerRef.value = null;
  }

  isLaunching.value = true; // 开始发射时设置状态

  let fired = 0;
  timerRef.value = setInterval(() => {
    mittBus.emit("triggerFireworks", src);
    fired++;

    // 达到指定次数后清除定时器
    if (fired >= count) {
      clearInterval(timerRef.value!);
      timerRef.value = null;
      isLaunching.value = false; // 发射完成后解除禁用
    }
  }, 1000);
};

// 简化后的处理函数
const handleSingleLaunch = () => {
  mittBus.emit("triggerFireworks");
};

const handleMultipleLaunch = (src?: string) => {
  triggerFireworks(10, src);
};

const handleImageLaunch = (src: string) => {
  mittBus.emit("triggerFireworks", src);
};

// 组件卸载时清理定时器
onUnmounted(() => {
  if (timerRef.value) {
    clearInterval(timerRef.value);
    timerRef.value = null;
  }
});

// 模拟新闻消息数据
const news = ref([
  {
    id: 1,
    title: "🎉 Just Enough Stack v1.0 正式发布！",
    content:
      "轻量级全栈开发框架正式上线，提供用户认证、权限管理、CRUD 示例等通用功能",
    time: "2025-12-25 10:00",
    type: "success",
  },
  {
    id: 2,
    title: "✨ 任务管理功能上线",
    content: "完整的任务 CRUD 功能已集成，支持状态管理、优先级设置和截止日期",
    time: "2025-12-25 10:30",
    type: "success",
  },
  {
    id: 3,
    title: "📖 开源项目说明",
    content:
      "本项目基于 FastAPI + Vue3 构建，提供最小化但完整的全栈开发基础设施",
    time: "2025-12-25 11:00",
    type: "success",
  },
]);

// 功能卡片数据
const features = [
  {
    title: "任务管理",
    description: "创建、管理和跟踪你的任务",
    icon: "TrendCharts",
    path: ROUTES.TASKS,
    color: "#67C23A",
  },
  {
    title: "个人中心",
    description: "查看和编辑个人资料信息",
    icon: "DataAnalysis",
    path: ROUTES.PROFILE,
    color: "#E6A23C",
  },
  {
    title: "首页",
    description: "返回系统首页仪表板",
    icon: "Shop",
    path: ROUTES.DASHBOARD,
    color: "#E2C4D6",
  },
];

const navigateToFeature = (path: string) => {
  router.push(path);
};

// 图标映射
const icons: Record<string, any> = {
  UploadFilled,
  TrendCharts,
  DataAnalysis,
  Shop,
};
</script>

<template>
  <div class="home-page">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h1>JUST ENOUGH STACK</h1>
      <p class="welcome-text">轻量级全栈开发框架 v1.0.0</p>

      <!-- 烟花触发按钮 -->
      <div class="fireworks-section">
        <h3 style="margin-bottom: 15px; color: #606266">
          🎉 热烈庆祝 Just Enough Stack 正式开源！
        </h3>
        <div class="fireworks-buttons">
          <el-button :disabled="isLaunching" @click="handleSingleLaunch">
            ✨ 放个小礼花
          </el-button>
          <el-button :disabled="isLaunching" @click="handleImageLaunch(bp)">
            🧧 打开幸运红包
          </el-button>
          <el-button :disabled="isLaunching" @click="handleMultipleLaunch()">
            🎆 璀璨烟火秀
          </el-button>
          <!-- <el-button :disabled="isLaunching" @click="handleImageLaunch(sd)">
            ❄️ 飘点小雪花
          </el-button>
          <el-button :disabled="isLaunching" @click="handleMultipleLaunch(sd)">
            ❄️ 浪漫暴风雪
          </el-button> -->
        </div>
        <p style="font-size: 0.5rem; color: #909399; margin-top: 10px">
          提示：也可以使用快捷键 Ctrl/Cmd + Shift + F 触发烟花
        </p>
      </div>
    </div>

    <!-- 功能区域 -->
    <div class="features-section">
      <h2>主要功能</h2>
      <el-row :gutter="20">
        <el-col
          v-for="feature in features"
          :key="feature.title"
          :span="8"
          :sm="12"
          :xs="24"
        >
          <el-card
            class="feature-card"
            shadow="hover"
            @click="navigateToFeature(feature.path)"
          >
            <div class="feature-content">
              <div class="feature-icon" :style="{ color: feature.color }">
                <el-icon size="40">
                  <component :is="icons[feature.icon]" />
                </el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
              <el-button type="primary" :color="feature.color" size="small">
                立即使用
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快速开始 -->
    <div class="quick-start-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <h3>快速开始</h3>
          </div>
        </template>
        <el-steps :active="0" finish-status="success">
          <el-step title="打开冰箱" description="你刚刚打开冰箱门！" />
          <el-step title="塞进大象 🐘" description="大象正准备被塞进去！" />
          <el-step title="关闭冰箱门" description="冰箱门被关上了！（有时候关不上）" />
          <el-step title="恭喜你！🎉" description="你已经学会了怎么将大象塞进冰箱！" />
        </el-steps>
        <div class="quick-action">
          <el-button type="primary" size="large" @click="openBili">
            开始尝试将长颈鹿🦒塞进冰箱
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 新闻消息栏 -->
    <div class="news-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <h3>📢 系统公告</h3>
          </div>
        </template>
        <div class="news-container">
          <el-timeline>
            <el-timeline-item
              v-for="item in news.slice().reverse()"
              :key="item.id"
              :timestamp="item.time"
              placement="top"
              :type="item.type as 'success' | 'info' | 'warning' | 'primary' | 'danger'"
            >
              <el-card class="news-item" shadow="hover">
                <h4 class="news-title">{{ item.title }}</h4>
                <p class="news-content">{{ item.content }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h1 {
  font-size: 2rem;
  color: #303133;
  margin-bottom: 10px;
}

.welcome-text {
  font-size: 0.8rem;
  color: #606266;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.fireworks-section {
  margin-top: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.fireworks-section h3 {
  color: #fff !important;
  margin-bottom: 15px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.fireworks-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.fireworks-buttons .el-button {
  min-width: 120px;
  font-weight: 600;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.fireworks-buttons .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.fireworks-section p {
  color: rgba(255, 255, 255, 0.8) !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.stats-section {
  margin-bottom: 40px;
}

.todo-card {
  height: 300px;
  text-align: center;
  background: #f5f7fa; /* 或你想要的颜色 */
  border: 2px dashed #d3d3d3;
  transition: all 0.3s;
}

.todo-card:hover {
  border-color: #409eff;
  transform: translateY(-2px);
}

.todo-content {
  padding: 40px 20px;
}

.todo-text {
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #909399;
  font-weight: 500;
  letter-spacing: 2px;
}

.features-section {
  margin-bottom: 40px;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.feature-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: #409eff;
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.2);
}

.feature-content {
  text-align: center;
  padding: 20px 10px;
}

.feature-icon {
  margin-bottom: 16px;
}

.feature-content h3 {
  color: #303133;
  margin-bottom: 12px;
  font-size: 1.2rem;
}

.feature-content p {
  color: #606266;
  line-height: 1.5;
  margin-bottom: 20px;
  font-size: 0.9rem;
}

.quick-start-section {
  margin-bottom: 40px;
}

.card-header {
  display: flex;
  justify-content: center;
}

.card-header h3 {
  margin: 0;
  color: #303133;
}

.quick-action {
  text-align: center;
  margin-top: 30px;
}

.news-section {
  margin-bottom: 40px;
}

.news-container {
  width: 100%;
  /* max-height: 400px; */
  /* overflow-y: auto; */
}

.news-item {
  margin-bottom: 10px;
  border-left: 4px solid transparent;
  transition: all 0.3s;
}

.news-item:hover {
  border-left-color: #409eff;
  transform: translateX(4px);
}

.news-title {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  color: #303133;
  font-weight: 600;
}

.news-content {
  margin: 0;
  color: #606266;
  line-height: 1.5;
  font-size: 0.9rem;
}

/* 时间线样式优化 */
:deep(.el-timeline-item__timestamp) {
  color: #909399;
  font-size: 0.8rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-page {
    padding: 15px;
  }

  .welcome-section h1 {
    font-size: 2rem;
  }

  .fireworks-section {
    margin-top: 20px;
    padding: 15px;
  }

  .fireworks-buttons {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }

  .fireworks-buttons .el-button {
    min-width: 200px;
  }

  .stats-section {
    margin-bottom: 30px;
  }

  .todo-content {
    padding: 30px 15px;
  }

  .todo-text {
    font-size: 1.2rem;
  }

  .features-section {
    margin-bottom: 30px;
  }

  .feature-card {
    margin-bottom: 20px;
  }

  .news-section {
    margin-bottom: 30px;
  }

  .news-container {
    max-height: 300px;
  }

  .news-title {
    font-size: 1rem;
  }

  .news-content {
    font-size: 0.85rem;
  }
}
</style>
