import { userService } from '@/api/user'
import type { Router } from 'vue-router'

export class AuthMiddleware {
    private router: Router

    constructor(router: Router) {
        this.router = router
    }

    // 检查用户是否已认证
    isAuthenticated(): boolean {
        return userService.isAuthenticated()
    }

    // 获取当前用户token
    getToken(): string | null {
        return userService.getToken()
    }

    // 认证守卫 - 要求登录
    requireAuth() {
        return (_to: any, _from: any, next: any) => {
            if (this.isAuthenticated()) {
                next()
            } else {
                next('/user/login')
            }
        }
    }

    // 游客守卫 - 已登录用户不能访问
    guestOnly() {
        return (_to: any, _from: any, next: any) => {
            if (!this.isAuthenticated()) {
                next()
            } else {
                next('/dashboard')
            }
        }
    }

    // 权限检查守卫
    hasPermission(_permission: string) {
        return (_to: any, _from: any, next: any) => {
            if (this.isAuthenticated()) {
                // 这里可以添加权限检查逻辑
                // 暂时简单通过
                next()
            } else {
                next('/user/login')
            }
        }
    }

    // 登出用户
    async logout(): Promise<void> {
        await userService.logout()
        this.router.push('/user/login')
    }

    // 设置认证拦截器
    setupInterceptors() {
        // 这里可以设置全局的HTTP拦截器
        // 比如自动添加token到请求头
        // 处理401错误自动跳转登录等
    }
}

// 导出单例
let authMiddleware: AuthMiddleware | null = null

export const createAuthMiddleware = (router: Router): AuthMiddleware => {
    if (!authMiddleware) {
        authMiddleware = new AuthMiddleware(router)
    }
    return authMiddleware
}

export const getAuthMiddleware = (): AuthMiddleware => {
    if (!authMiddleware) {
        throw new Error('AuthMiddleware not initialized. Call createAuthMiddleware first.')
    }
    return authMiddleware
}
