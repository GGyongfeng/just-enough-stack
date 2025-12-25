import axios, { AxiosError } from 'axios';
import { requestLogger } from '../middleware/requestLogger';
import type { StandardResponse } from '@/types/api';

// 创建 axios 实例
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器 - 添加认证 token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器 - 统一错误处理
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error: AxiosError) => {
        // 处理认证错误
        if (error.response?.status === 401) {
            localStorage.removeItem('access_token');
            // 可以在这里添加跳转到登录页的逻辑
            window.location.href = '/login';
        }

        // 处理其他错误
        console.error('API Error:', {
            status: error.response?.status,
            message: error.message,
            url: error.config?.url
        });

        return Promise.reject(error);
    }
);

// 设置请求监控中间件
requestLogger.setupInterceptors(api);

// API 客户端类，提供与原 ApiClient 相同的接口
export class ApiClient {
    // 获取认证token
    public getAuthToken(): string | null {
        return localStorage.getItem('access_token');
    }

    // 设置认证token
    public setAuthToken(token: string): void {
        localStorage.setItem('access_token', token);
    }

    // 清除认证token
    public clearAuthToken(): void {
        localStorage.removeItem('access_token');
    }

    // GET请求
    public async get<T>(endpoint: string, params?: Record<string, any>): Promise<StandardResponse<T>> {
        const response = await api.get<StandardResponse<T>>(endpoint, { params });
        return response.data;
    }

    // POST请求
    public async post<T>(endpoint: string, data?: any): Promise<StandardResponse<T>> {
        const response = await api.post<StandardResponse<T>>(endpoint, data);
        return response.data;
    }

    // PUT请求
    public async put<T>(endpoint: string, data?: any): Promise<StandardResponse<T>> {
        const response = await api.put<StandardResponse<T>>(endpoint, data);
        return response.data;
    }

    // DELETE请求
    public async delete<T>(endpoint: string): Promise<StandardResponse<T>> {
        const response = await api.delete<StandardResponse<T>>(endpoint);
        return response.data;
    }
}

// 导出实例
export const apiClient = new ApiClient();
export default api;