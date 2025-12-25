import type { PaginationResponse } from "./api";

// query 相关类型
export interface QueryType {
  id: number;
  query_name: string;
  category_id?: number;
  lazy_query: string;
  query_detail?: string;
  extra?: string;
  query_comment?: string;
  creator_id: number;
  query_category_fullname?: string;
  creator_nickname?: string;
  creator_full_name?: string;
  creator_username?: string;
  created_at: string;
  updated_at?: string;
  // 兼容字段
  title?: string;
  description?: string;
  priority?: number;
  difficulty?: number;
  tags?: string[];
  status?: "pending" | "running" | "completed" | "failed";
}

export interface QueryCreateRequest {
  lazy_query?: string;
  detail_query?: string;
  priority?: number;
  title?: string;
  description?: string;
  difficulty?: number;
  tags?: string[];
}

export interface QueryUpdateRequest {
  lazy_query?: string;
  detail_query?: string;
  priority?: number;
  title?: string;
  description?: string;
  status?: "pending" | "running" | "completed" | "failed";
  difficulty?: number;
  tags?: string[];
}
export interface QueryListResponse {
  queries: QueryType[];
  pagination: PaginationResponse;
}
