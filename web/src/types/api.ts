// API响应标准格式
export interface StandardResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

// 成功页面消息类型
export interface SuccessPageMessage {
  type: "success" | "warning" | "error" | "info";
  title: string;
  message: string;
  details?: string[];
  showReturnButton?: boolean;
  returnPath?: string;
  returnText?: string;
}

// 分页相关类型
export interface PaginationRequest {
  page: number;
  size: number;
}

export interface PaginationResponse {
  page: number;
  size: number;
  total: number;
  pages: number;
}

// 用户相关类型
export interface User {
  id: number;
  username: string;
  nickname?: string;
  full_name?: string;
  created_at: string;
  updated_at?: string;
}

export interface UserRegisterRequest {
  username: string;
  password: string;
  nickname?: string;
  full_name?: string;
  register_token: string;
}

export interface UserLoginRequest {
  username: string;
  password: string;
}

export interface UserUpdateRequest {
  nickname?: string;
  full_name?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// 评估相关类型
export interface Evaluation {
  id: number;
  query_id: number;
  query_name?: string;
  agent_id: number;
  agent_name?: string;
  trajectory?: string;
  eval_report?: string;
  eval_comment?: string;
  total_score?: number;
  comparable_items?: string;
  extra?: string;
  creator_id?: number;
  deliverables?: Array<{
    id: number;
    filename: string;
    content: string;
    file_type: string;
    file_size: number;
    deliverables_comment?: string;
    extra?: string;
    created_at?: string;
    updated_at?: string;
  }>;
  created_at: string;
  updated_at?: string;
  // 向后兼容的字段
  evaluator_id?: number;
  score?: number;
  feedback?: string;
  evaluation_criteria?: string;
  status?: string;
  version?: string;
  agent?: string;
  duration?: number;
  rounds?: number;
  report_content?: string;
}

// 文件数据模型（Base64编码）
export interface FileDataModelBase64 {
  filename: string;
  content: string;
  encoding: string;
  file_type: string;
  file_size: number;
  extra?: Record<string, any>;
}

// 根据后端最新格式更新的评估创建请求
export interface EvaluationCreateRequest {
  query_id: number;
  agent_id: number;
  trajectory?: string;
  eval_report?: string;
  eval_comment?: string;
  total_score?: number;
  comparable_items?: string;
  extra?: string;
  deliverables?: FileDataModelBase64[];
}

export interface EvaluationUpdateRequest {
  score?: number;
  feedback?: string;
  evaluation_criteria?: string;
  status?: string;
  version?: string;
  agent?: string;
  duration?: number;
  rounds?: number;
  trajectory?: string;
  report_content?: string;
}
export interface EvaluationListResponse {
  evaluations: Evaluation[];
  pagination: PaginationResponse;
}

// 交付文件相关类型
export interface Deliverable {
  id: number;
  evaluation_id: number;
  file_name: string;
  file_type?: string;
  file_size?: number;
  file_path?: string;
  upload_time: string;
  description?: string;
}

export interface DeliverableCreateRequest {
  evaluation_id: number;
  file_name: string;
  file_type?: string;
  file_size?: number;
  file_content: string; // base64编码
  description?: string;
}

export interface DeliverableListResponse {
  deliverables: Deliverable[];
  pagination: PaginationResponse;
}

// 文件信息类型
export interface FileInfo {
  file_id: number;
  file_name: string;
  file_size: number;
  file_type: string;
  upload_time: string;
}

export interface FileContent {
  file_content: string; // base64编码
  file_name: string;
  file_type: string;
}
