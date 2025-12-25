<template>
  <div class="user-profile">
    <div class="profile-header">
      <h1>个人资料</h1>
      <p>管理您的账户信息</p>
    </div>

    <div class="profile-content">
      <!-- 用户信息展示 -->
      <div class="profile-card" v-if="userInfo && !isEditing">
        <div class="card-header">
          <h2>基本信息</h2>
          <button @click="startEdit" class="edit-btn">编辑</button>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <label>用户名</label>
            <span>{{ userInfo.username }}</span>
          </div>
          <div class="info-item">
            <label>昵称</label>
            <span>{{ userInfo.nickname || "未设置" }}</span>
          </div>
          <div class="info-item">
            <label>全名</label>
            <span>{{ userInfo.full_name || "未设置" }}</span>
          </div>
          <div class="info-item">
            <label>注册时间</label>
            <span>{{ formatDate(userInfo.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 编辑表单 -->
      <div class="profile-card" v-if="isEditing">
        <div class="card-header">
          <h2>编辑信息</h2>
          <div class="action-buttons">
            <button @click="cancelEdit" class="cancel-btn">取消</button>
            <button @click="saveProfile" class="save-btn" :disabled="saving">
              {{ saving ? "保存中..." : "保存" }}
            </button>
          </div>
        </div>
        <form @submit.prevent="saveProfile" class="edit-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              id="username"
              type="text"
              :value="userInfo?.username"
              disabled
              class="disabled-input"
            />
            <small>用户名不可修改</small>
          </div>
          <div class="form-group">
            <label for="nickname">昵称</label>
            <input
              id="nickname"
              type="text"
              v-model="editForm.nickname"
              placeholder="请输入昵称"
            />
          </div>
          <div class="form-group">
            <label for="fullName">全名</label>
            <input
              id="fullName"
              type="text"
              v-model="editForm.full_name"
              placeholder="请输入全名"
            />
          </div>
        </form>
      </div>

      <!-- 操作区域 -->
      <div class="profile-actions">
        <div class="common-actions">
          <h3>账户操作</h3>
          <div class="common-actions-buttons">
            <button @click="showDeleteConfirm = true" class="common-btn delete-btn">
              账户注销
            </button>
            <button @click="handleLogout" class="common-btn logout-btn">退出登录</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div
      v-if="showDeleteConfirm"
      class="modal-overlay"
      @click="showDeleteConfirm = false"
    >
      <div class="modal" @click.stop ref="modalRef" @mousemove="handleMouseMove">
        <h3>确认删除账户</h3>
        <p>此操作不可逆，将永久删除您的账户和所有相关数据。</p>
        <div class="modal-actions">
          <button @click="showDeleteConfirm = false" class="cancel-btn">取消</button>
          <div class="escape-button-container">
            <button
              ref="deleteButtonRef"
              @click="deleteAccount"
              class="delete-commit-btn"
              :class="{ escaping: isButtonEscaping, caught: isButtonCaught }"
              :disabled="deleting"
            >
              {{ deleting ? "删除中..." : isButtonCaught ? "被抓住了！🎉" : "确认删除" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误信息 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { userService } from "@/api/user";
import type { User, UserUpdateRequest } from "@/types/api";
import { ElMessage } from "element-plus";

const router = useRouter();

// 响应式数据
const userInfo = ref<User | null>(null);
const loading = ref(false);
const saving = ref(false);
const deleting = ref(false);
const error = ref("");
const isEditing = ref(false);
const showDeleteConfirm = ref(false);

// 逃跑按钮相关状态
const isButtonEscaping = ref(false);
const isButtonCaught = ref(false);

// DOM引用
const modalRef = ref<HTMLElement>();
const deleteButtonRef = ref<HTMLElement>();

// 编辑表单数据
const editForm = ref<UserUpdateRequest>({
  nickname: "",
  full_name: "",
});

// 计算两点间距离
const getDistance = (x1: number, y1: number, x2: number, y2: number): number => {
  return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
};

// 添加去抖动变量
let lastMoveTime = 0;
let escapeTimeout: ReturnType<typeof setTimeout> | null = null;

// 处理鼠标移动事件
const handleMouseMove = (event: MouseEvent) => {
  if (!modalRef.value || !deleteButtonRef.value || isButtonCaught.value) return;

  // 去抖动：限制处理频率，避免抽搐
  const now = Date.now();
  if (now - lastMoveTime < 16) return; // 约60fps限制
  lastMoveTime = now;

  const modalRect = modalRef.value.getBoundingClientRect();
  const buttonRect = deleteButtonRef.value.getBoundingClientRect();

  // 按钮中心点（相对于modal）
  const buttonCenterX = buttonRect.left - modalRect.left + buttonRect.width / 2;
  const buttonCenterY = buttonRect.top - modalRect.top + buttonRect.height / 2;

  // 鼠标位置（相对于modal）
  const relativeMouseX = event.clientX - modalRect.left;
  const relativeMouseY = event.clientY - modalRect.top;

  const distance = getDistance(
    buttonCenterX,
    buttonCenterY,
    relativeMouseX,
    relativeMouseY
  );

  // 增加危险区域，让按钮更敏感（更难抓住）
  if (distance < 150) {
    // 清除之前的超时
    if (escapeTimeout) {
      clearTimeout(escapeTimeout);
    }

    isButtonEscaping.value = true;

    // 计算逃跑方向（远离鼠标）
    const deltaX = buttonCenterX - relativeMouseX;
    const deltaY = buttonCenterY - relativeMouseY;
    const angle = Math.atan2(deltaY, deltaX);

    // 动态逃跑距离：距离越近，逃得越远
    const escapeDistance = Math.max(120, 250 - distance);

    // 添加预测性移动：预测鼠标下一步位置
    const mouseSpeedX = event.movementX || 0;
    const mouseSpeedY = event.movementY || 0;
    const predictiveX = relativeMouseX + mouseSpeedX * 3;
    const predictiveY = relativeMouseY + mouseSpeedY * 3;

    // 重新计算相对于预测位置的逃跑方向
    const predictiveDeltaX = buttonCenterX - predictiveX;
    const predictiveDeltaY = buttonCenterY - predictiveY;
    const predictiveAngle = Math.atan2(predictiveDeltaY, predictiveDeltaX);

    let newX = buttonCenterX + Math.cos(predictiveAngle) * escapeDistance;
    let newY = buttonCenterY + Math.sin(predictiveAngle) * escapeDistance;

    // 添加更多随机性和智能躲避
    const randomAngle = (Math.random() - 0.5) * Math.PI * 0.8; // 更大的随机角度
    newX += Math.cos(angle + randomAngle) * (60 + Math.random() * 80);
    newY += Math.sin(angle + randomAngle) * (60 + Math.random() * 80);

    // 计算相对于按钮中心点的偏移
    const offsetX = newX - buttonCenterX;
    const offsetY = newY - buttonCenterY;

    // 应用变换，添加更多动画效果
    const rotateAngle = (Math.random() - 0.5) * 40; // 更大的旋转角度
    const scaleValue = 0.95 + Math.random() * 0.2; // 随机缩放
    deleteButtonRef.value.style.transform = `translate(${offsetX}px, ${offsetY}px) rotate(${rotateAngle}deg) scale(${scaleValue})`;
    deleteButtonRef.value.style.transition =
      "transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)";

    // 延迟移除escaping状态，防止抽搐
    escapeTimeout = setTimeout(() => {
      isButtonEscaping.value = false;
      if (deleteButtonRef.value) {
        deleteButtonRef.value.style.transition = "transform 0.3s ease";
      }
    }, 400);
  } else if (distance > 300) {
    // 增加安全距离
    if (escapeTimeout) {
      clearTimeout(escapeTimeout);
    }
    isButtonEscaping.value = false;
    if (deleteButtonRef.value) {
      deleteButtonRef.value.style.transition = "transform 0.3s ease";
    }
  }
};

// 获取用户信息
const fetchUserProfile = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await userService.getCurrentUserProfile();
    if (response.success && response.data?.user) {
      userInfo.value = response.data.user;
    } else {
      error.value = response.message || "获取用户信息失败";
    }
  } catch (err) {
    error.value = "获取用户信息失败，请重试";
    console.error("获取用户信息失败:", err);
  } finally {
    loading.value = false;
  }
};

// 开始编辑
const startEdit = () => {
  if (userInfo.value) {
    editForm.value = {
      nickname: userInfo.value.nickname || "",
      full_name: userInfo.value.full_name || "",
    };
  }
  isEditing.value = true;
};

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false;
  editForm.value = {
    nickname: "",
    full_name: "",
  };
};

// 保存用户信息
const saveProfile = async () => {
  try {
    saving.value = true;
    error.value = "";

    const response = await userService.updateCurrentUserProfile(editForm.value);
    if (response.success) {
      // 更新本地用户信息
      if (userInfo.value) {
        userInfo.value.nickname = editForm.value.nickname;
        userInfo.value.full_name = editForm.value.full_name;
      }
      isEditing.value = false;
      // 可以显示成功提示
    } else {
      error.value = response.message || "更新失败";
    }
  } catch (err) {
    error.value = "更新失败，请重试";
    console.error("更新用户信息失败:", err);
  } finally {
    saving.value = false;
  }
};

// 删除账户
const deleteAccount = async () => {
  // 如果按钮还没被"抓住"，先标记为被抓住
  if (!isButtonCaught.value) {
    isButtonCaught.value = true;

    // 显示成功信息
    ElMessage.success(`🎉 恭喜！点中了逃跑的按钮！`);

    // 3秒后重置状态，实际执行删除逻辑
    setTimeout(() => {
      ElMessage.warning("坏消息，删除功能已被禁用！点中了也不管用 🤣");
      resetButtonState();
    }, 2000);

    return;
  }
};

// 重置按钮状态
const resetButtonState = () => {
  isButtonEscaping.value = false;
  isButtonCaught.value = false;

  if (deleteButtonRef.value) {
    deleteButtonRef.value.style.transform = "";
  }
};

// 退出登录
const handleLogout = async () => {
  try {
    await userService.logout();
    router.push("/user/login");
  } catch (err) {
    console.error("退出登录失败:", err);
    // 即使退出失败也跳转到登录页
    router.push("/user/login");
  }
};

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString("zh-CN");
};

// 监听删除确认对话框的显示/隐藏，重置按钮状态
const handleDeleteConfirmChange = (newVal: boolean) => {
  if (!newVal) {
    // 对话框关闭时重置按钮状态
    nextTick(() => {
      resetButtonState();
    });
  }
};

// 监听 showDeleteConfirm 变化
import { watch } from "vue";
watch(showDeleteConfirm, handleDeleteConfirmChange);

// 组件挂载时获取用户信息
onMounted(() => {
  fetchUserProfile();
});
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  margin-bottom: 30px;
}

.profile-header h1 {
  font-size: 2rem;
  color: #333;
  margin: 0 0 8px 0;
}

.profile-header p {
  color: #666;
  margin: 0;
}

.profile-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.card-header h2 {
  margin: 0;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: 600;
  color: #555;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

.info-item span {
  color: #333;
  padding: 8px 0;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
}

.form-group input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.disabled-input {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.form-group small {
  color: #666;
  font-size: 0.875rem;
  margin-top: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.edit-btn,
.save-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.edit-btn:hover,
.save-btn:hover {
  background: #0056b3;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.cancel-btn:hover {
  background: #545b62;
}

.profile-actions {
  margin-top: 40px;
}

.common-actions {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.common-actions h3 {
  color: #495057;
  margin: 0 0 16px 0;
}

.common-actions-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.common-btn {
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  color: white;
}

.logout-btn {
  background: #6c757d;
}

.logout-btn:hover {
  background: #5a6268;
}

.delete-btn {
  background: #dc3545;
}

.delete-btn:hover {
  background: #c82333;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
  min-height: 200px;
  position: relative;
}

.modal h3 {
  margin: 0 0 12px 0;
  color: #333;
}

.modal p {
  margin: 0 0 20px 0;
  color: #666;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  position: absolute;
  bottom: 24px;
  right: 24px;
}

/* 逃跑按钮样式 */
.escape-button-container {
  position: relative;
  display: inline-block;
}

.delete-commit-btn {
  background: #cb444a;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(203, 68, 74, 0.3);
  position: relative;
  z-index: 2;
  transform-origin: center center;
}

.delete-commit-btn.escaping {
  background: #e74c3c;
  box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
  z-index: 10;
  transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.delete-commit-btn.caught {
  background: #27ae60 !important;
  animation: celebration 0.6s ease-in-out;
  transform: scale(1.1) !important;
}

@keyframes celebration {
  0%,
  100% {
    transform: scale(1.1) rotate(0deg);
    box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
  }
  25% {
    transform: scale(1.2) rotate(-5deg);
    box-shadow: 0 8px 25px rgba(39, 174, 96, 0.6);
  }
  75% {
    transform: scale(1.2) rotate(5deg);
    box-shadow: 0 8px 25px rgba(39, 174, 96, 0.6);
  }
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin: 16px 0;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
