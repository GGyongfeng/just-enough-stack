<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <template #header>
        <div class="login-header">
          <h2 class="login-title">用户登录</h2>
          <p class="login-subtitle">欢迎回到 Agent 评估系统</p>
        </div>
      </template>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        size="large"
        @submit.prevent="handleLogin"
        autocomplete="off"
        data-lpignore="true"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
            :disabled="loading"
            autocomplete="username"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
            :disabled="loading"
            @keyup.enter="handleLogin"
            autocomplete="current-password"
            data-lpignore="true"
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="loginForm.rememberMe" :disabled="loading">
            记住我
          </el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            style="width: 100%"
            size="large"
            :loading="loading"
            :disabled="loading"
          >
            {{ loading ? "登录中..." : "登录" }}
          </el-button>
        </el-form-item>

        <el-alert
          v-if="errorMessage"
          :title="errorMessage"
          type="error"
          :closable="false"
          style="margin-top: 16px"
        />
      </el-form>

      <div class="register-link">
        <span>还没有账号？</span>
        <router-link to="/user/register">立即注册</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { UserLoginRequest } from '@/types/api'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)
const errorMessage = ref('')

// 登录表单数据
const loginForm = reactive<UserLoginRequest & { rememberMe: boolean }>({
  username: '',
  password: '',
  rememberMe: false
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应为 3-50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    // 验证表单
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true
    errorMessage.value = ''

    // 调用 store 中的登录方法
    const success = await userStore.login(loginForm.username, loginForm.password)

    if (success) {
      ElMessage.success('登录成功！')
      // 登录成功后跳转到仪表板
      router.push('/')
    } else {
      errorMessage.value = userStore.error || '登录失败'
      ElMessage.error(errorMessage.value)
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    errorMessage.value = error.message || '登录失败，请检查用户名和密码'
    ElMessage.error(errorMessage.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--el-color-primary-light) 0%, var(--el-color-primary-light) 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
}

.login-title {
  margin: 0 0 8px 0;
  color: var(--el-bg-color);
  font-size: 1.8rem;
  font-weight: 600;
}

.login-subtitle {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.register-link {
  text-align: center;
  margin-top: 16px;
  font-size: 0.9rem;
  color: var(--el-text-color-secondary);
}

.register-link a {
  color: var(--el-color-primary-light);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Element Plus 组件样式覆盖 */
:deep(.el-card__header) {
  background: linear-gradient(135deg, var(--el-color-primary-light) 0%, var(--el-color-primary-light) 100%);
  color: var(--el-bg-color);
  text-align: center;
  padding: 24px;
}

:deep(.el-card__body) {
  padding: 32px 24px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, var(--el-color-primary-light) 0%, var(--el-color-primary-light) 100%);
  border: none;
  border-radius: 8px;
  font-weight: 500;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, var(--el-color-primary-light-3) 0%, var(--el-color-primary-light) 100%);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 16px;
  }

  .login-card {
    max-width: 100%;
  }

  :deep(.el-card__header) {
    padding: 20px;
  }

  :deep(.el-card__body) {
    padding: 24px 20px;
  }

  .login-title {
    font-size: 1.5rem;
  }
}
</style>
