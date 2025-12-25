import { apiClient } from '@/api/client'
import type {
    StandardResponse,
    User,
    UserRegisterRequest,
    UserLoginRequest,
    UserUpdateRequest,
    LoginResponse,
} from '@/types/api'

export class UserService {
    // 用户注册
    async register(userData: UserRegisterRequest): Promise<StandardResponse<{ user: User }>> {
        return apiClient.post('/user/register', userData)
    }

    // 用户登录
    async login(credentials: UserLoginRequest): Promise<StandardResponse<LoginResponse>> {
        const response = await apiClient.post<LoginResponse>('/user/login', credentials)

        // 登录成功后保存token
        if (response.success && response.data?.access_token) {
            apiClient.setAuthToken(response.data.access_token)
        }

        return response
    }

    // 用户登出
    async logout(): Promise<void> {
        apiClient.clearAuthToken()
    }

    // 获取当前用户信息
    async getCurrentUserProfile(): Promise<StandardResponse<{ user: User }>> {
        return apiClient.get('/user/profile')
    }

    // 更新当前用户信息
    async updateCurrentUserProfile(updateData: UserUpdateRequest): Promise<StandardResponse> {
        return apiClient.put('/user/profile', updateData)
    }

    // 根据用户名获取用户信息
    async getUserByUsername(username: string): Promise<StandardResponse<{ user: User }>> {
        return apiClient.get(`/user/${username}`)
    }

    // 删除用户账户
    async deleteUser(username: string): Promise<StandardResponse> {
        return apiClient.delete(`/user/${username}`)
    }

    // 检查是否已登录
    isAuthenticated(): boolean {
        return !!apiClient.getAuthToken()
    }

    // 获取当前token
    getToken(): string | null {
        return apiClient.getAuthToken()
    }
}

// 导出默认实例
export const userService = new UserService()
export default userService
