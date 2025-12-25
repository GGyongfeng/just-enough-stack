<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { UserRegisterRequest } from '@/types/api'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const registerFormRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)
const errorMessage = ref('')

// 注册表单数据
const registerForm = reactive<UserRegisterRequest & { confirmPassword: string}>({
  username: '',
  password: '',
  nickname: '',
  full_name: '',
  confirmPassword: '',
  register_token: ''
})

// 表单验证规则
const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' },
    {
      validator: (_rule: any, value: any, callback: any) => {
        // 用户名只能包含英文字母、数字、下划线、连字符
        const usernamePattern = /^[a-zA-Z0-9_-]+$/
        if (!usernamePattern.test(value)) {
          callback(new Error('用户名只能包含英文字母、数字、下划线(_)和连字符(-)'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: any, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ],
  register_token: [
    { required: true, message: '请输入邀请码', trigger: 'blur' } // 邀请码为必填字段，不设格式限制
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    loading.value = true
    errorMessage.value = ''

    const registerData: any = {
      username: registerForm.username,
      password: registerForm.password,
      nickname: registerForm.nickname,
      full_name: registerForm.full_name,
      register_token: registerForm.register_token.trim()// 将 register_token 映射到 token 字段，现在是必填的
    }

    const success = await userStore.register(registerData)

    if (success) {
      ElMessage.success('注册成功！请登录')
      router.push('/user/login')
    } else {
      errorMessage.value = userStore.error || '注册失败'
    }
  } catch (error) {
    console.error('注册失败:', error)
    errorMessage.value = '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-container">
    <el-card class="register-card" shadow="always">
      <template #header>
        <div class="register-header">
          <h2 class="register-title">用户注册</h2>
          <p class="register-subtitle">欢迎加入 Agent 评估系统</p>
        </div>
      </template>

      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        size="large"
        @submit.prevent="handleRegister"
        autocomplete="off"
        data-lpignore="true"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            show-password
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="昵称" prop="nickname">
          <el-input
            v-model="registerForm.nickname"
            placeholder="请输入昵称"
            prefix-icon="Avatar"
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="全名（可选）">
          <el-input
            v-model="registerForm.full_name"
            placeholder="请输入真实姓名（可选）"
            prefix-icon="User"
            clearable
            :disabled="loading"
          />
        </el-form-item>

        <el-form-item label="邀请码" prop="register_token">
          <el-input
            v-model="registerForm.register_token"
            placeholder="请输入邀请码"
            prefix-icon="Ticket"
            clearable
            :disabled="loading"
          />
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
            {{ loading ? "注册中..." : "注册" }}
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

      <div class="login-link">
        <span>已有账号？</span>
        <router-link to="/user/login">立即登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--el-color-primary-light) 0%, var(--el-color-primary-light) 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 450px;
  border-radius: 16px;
  overflow: hidden;
}

.register-header {
  text-align: center;
  padding: 8px 0;
}

.register-title {
  margin: 0 0 8px 0;
  color: var(--el-text-color-primary);
  font-size: 28px;
  font-weight: 600;
}

.register-subtitle {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
  color: var(--el-text-color-secondary);
}

.login-link a {
  color: var(--el-color-primary-light);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
}

.login-link a:hover {
  text-decoration: underline;
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}

:deep(.el-input__inner) {
  border-radius: 8px;
}

:deep(.el-button--primary) {
  border-radius: 8px;
  font-weight: 500;
  font-size: 16px;
}
</style>
