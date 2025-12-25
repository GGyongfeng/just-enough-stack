import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userService } from '@/api/user'
import { apiClient } from '@/api/client'
import type { User, LoginResponse, UserRegisterRequest } from '@/types/api'

export const useUserStore = defineStore('user', () => {
    // 状态
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)
    const isLoggedIn = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    // 用户设置偏好
    const settings = ref({
        sidebarCollapsed: false
    })

    // 计算属性
    const isAuthenticated = computed(() => {
        return isLoggedIn.value && !!token.value
    })

    const userDisplayName = computed(() => {
        if (!user.value) return '未知用户'
        return user.value.nickname || user.value.full_name || user.value.username
    })

    // 动作
    const register = async (registerData: UserRegisterRequest): Promise<boolean> => {
        try {
            loading.value = true
            error.value = ''

            const response = await userService.register(registerData)

            if (response.success) {
                return true
            } else {
                error.value = response.message || '注册失败'
                return false
            }
        } catch (err) {
            error.value = '注册失败，请重试'
            console.error('注册错误:', err)
            return false
        } finally {
            loading.value = false
        }
    }

    const login = async (username: string, password: string): Promise<boolean> => {
        try {
            loading.value = true
            error.value = ''

            const response = await userService.login({ username, password })

            if (response.success && response.data) {
                const loginData: LoginResponse = response.data

                // 更新状态
                user.value = loginData.user
                token.value = loginData.access_token
                isLoggedIn.value = true

                // 保存到localStorage
                localStorage.setItem('user', JSON.stringify(loginData.user))
                localStorage.setItem('access_token', loginData.access_token)

                return true
            } else {
                error.value = response.message || '登录失败'
                return false
            }
        } catch (err) {
            error.value = '登录失败，请重试'
            console.error('登录错误:', err)
            return false
        } finally {
            loading.value = false
        }
    }

    const logout = async (): Promise<void> => {
        try {
            await userService.logout()
        } finally {
            // 清理状态
            user.value = null
            token.value = null
            isLoggedIn.value = false
            error.value = ''

            // 清理localStorage
            localStorage.removeItem('user')
            localStorage.removeItem('access_token')
        }
    }

    const fetchUserProfile = async (): Promise<boolean> => {
        try {
            loading.value = true
            error.value = ''

            const response = await userService.getCurrentUserProfile()

            if (response.success && response.data?.user) {
                user.value = response.data.user
                // 更新localStorage中的用户信息
                localStorage.setItem('user', JSON.stringify(response.data.user))
                return true
            } else {
                error.value = response.message || '获取用户信息失败'
                return false
            }
        } catch (err) {
            error.value = '获取用户信息失败'
            console.error('获取用户信息错误:', err)
            return false
        } finally {
            loading.value = false
        }
    }

    const updateProfile = async (updateData: { nickname?: string; full_name?: string }): Promise<boolean> => {
        try {
            loading.value = true
            error.value = ''

            const response = await userService.updateCurrentUserProfile(updateData)

            if (response.success) {
                // 更新本地用户信息
                if (user.value) {
                    user.value.nickname = updateData.nickname || user.value.nickname
                    user.value.full_name = updateData.full_name || user.value.full_name
                    localStorage.setItem('user', JSON.stringify(user.value))
                }
                return true
            } else {
                error.value = response.message || '更新失败'
                return false
            }
        } catch (err) {
            error.value = '更新失败，请重试'
            console.error('更新用户信息错误:', err)
            return false
        } finally {
            loading.value = false
        }
    }

    const initializeFromStorage = (): void => {
        try {
            const storedUser = localStorage.getItem('user')
            const storedToken = localStorage.getItem('access_token')
            const storedSettings = localStorage.getItem('userSettings')

            if (storedUser && storedToken) {
                user.value = JSON.parse(storedUser)
                token.value = storedToken
                isLoggedIn.value = true
                // 重要：同时设置apiClient的token
                apiClient.setAuthToken(storedToken)
            }

            if (storedSettings) {
                settings.value = { ...settings.value, ...JSON.parse(storedSettings) }
            }
        } catch (error) {
            console.error('初始化用户状态失败:', error)
            // 清理可能损坏的数据
            localStorage.removeItem('user')
            localStorage.removeItem('access_token')
            localStorage.removeItem('userSettings')
        }
    }

    const updateSettings = (newSettings: Partial<typeof settings.value>): void => {
        settings.value = { ...settings.value, ...newSettings }
        localStorage.setItem('userSettings', JSON.stringify(settings.value))
    }

    const clearError = (): void => {
        error.value = ''
    }

    return {
        // 状态
        user,
        token,
        isLoggedIn,
        loading,
        error,
        settings,

        // 计算属性
        isAuthenticated,
        userDisplayName,

        // 动作
        register,
        login,
        logout,
        fetchUserProfile,
        updateProfile,
        initializeFromStorage,
        updateSettings,
        clearError,
    }
})
