import {
  AxiosInstance,
  InternalAxiosRequestConfig,
  AxiosResponse,
} from "axios";

interface RequestLog {
  timestamp: string;
  method: string;
  url: string;
  requestBody?: any;
  responseData?: any;
  responseStatus: number;
  duration: number;
}

class RequestLogger {
  private logs: RequestLog[] = [];

  setupInterceptors(axiosInstance: AxiosInstance) {
    // 请求拦截器
    axiosInstance.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        config.metadata = {
          startTime: Date.now(),
          timestamp: new Date().toISOString(),
        };

        console.log("🚀 API请求:", {
          method: config.method?.toUpperCase(),
          url: config.url,
          baseURL: config.baseURL,
          headers: config.headers,
          data: config.data,
          params: config.params,
        });

        return config;
      },
      (error) => {
        console.error("❌ 请求错误:", error);
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    axiosInstance.interceptors.response.use(
      (response: AxiosResponse) => {
        const endTime = Date.now();
        const startTime = response.config.metadata?.startTime || endTime;
        const duration = endTime - startTime;

        const log: RequestLog = {
          timestamp:
            response.config.metadata?.timestamp || new Date().toISOString(),
          method: response.config.method?.toUpperCase() || "GET",
          url: `${response.config.baseURL || ""}${response.config.url || ""}`,
          requestBody: response.config.data,
          responseData: response.data,
          responseStatus: response.status,
          duration,
        };

        this.logs.push(log);

        console.log("✅ API响应:", {
          method: log.method,
          url: log.url,
          status: response.status,
          duration: `${duration}ms`,
          data: response.data,
        });

        return response;
      },
      (error) => {
        const endTime = Date.now();
        const startTime = error.config?.metadata?.startTime || endTime;
        const duration = endTime - startTime;

        const log: RequestLog = {
          timestamp:
            error.config?.metadata?.timestamp || new Date().toISOString(),
          method: error.config?.method?.toUpperCase() || "GET",
          url: `${error.config?.baseURL || ""}${error.config?.url || ""}`,
          requestBody: error.config?.data,
          responseData: error.response?.data,
          responseStatus: error.response?.status || 0,
          duration,
        };

        this.logs.push(log);

        console.error("❌ API错误:", {
          method: log.method,
          url: log.url,
          status: error.response?.status,
          duration: `${duration}ms`,
          error: error.response?.data || error.message,
        });

        return Promise.reject(error);
      }
    );
  }

  getLogs(): RequestLog[] {
    return this.logs;
  }

  clearLogs(): void {
    this.logs = [];
  }

  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

export const requestLogger = new RequestLogger();
export default RequestLogger;

// 扩展 AxiosRequestConfig 类型
declare module "axios" {
  interface AxiosRequestConfig {
    metadata?: {
      startTime: number;
      timestamp: string;
    };
  }
}
