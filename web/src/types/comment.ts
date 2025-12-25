/**
 * 评论系统类型定义
 * 后端只存储 json 格式的string 和 提供API
 * 前端使用结构化的对象 来渲染
 * 所有的 comment 统一结构
 */

export interface CommentItem {
  id: string;
  content: string;
  author: string;
  authorId?: number;
  created_at: string;
  updatedAt?: string;
  parentId?: string; // 用于回复评论
  isEditing?: boolean; // 前端状态：是否正在编辑
  isDeleted?: boolean; // 前端状态：是否已删除
  showReplyForm?: boolean; // 前端状态：是否显示回复表单
  isLiked?: boolean; // 前端状态：当前用户是否点赞
  likeCount?: number; // 点赞数
  replies?: CommentItem[]; // 子回复
}

export interface CommentThread {
  items: CommentItem[];
  total: number;
  hasMore?: boolean;
}

export type CommentType = "deliverable" | "evaluation";

export interface CommentData {
  type: CommentType;
  targetId: number; // deliverable_id 或 evaluation_id
  thread: CommentThread;
  lastModified?: string;
}

// 用于前端状态管理的评论存储结构
export interface CommentStore {
  deliverables: Record<number, CommentThread>; // deliverable_id -> CommentThread
  evaluations: Record<number, CommentThread>; // evaluation_id -> CommentThread
}

// 创建新评论的请求数据
export interface CreateCommentRequest {
  content: string;
  parentId?: string; // 回复评论时使用
}

// 更新评论的请求数据
export interface UpdateCommentRequest {
  content: string;
}

// 评论操作的响应
export interface CommentOperationResponse {
  success: boolean;
  message: string;
  data?: CommentItem;
}

// 工具函数：将后端的字符串评论转换为前端结构
export function parseCommentString(
  commentStr: string | null | undefined
): CommentThread {
  if (!commentStr || commentStr.trim() === "") {
    return {
      items: [],
      total: 0,
      hasMore: false,
    };
  }

  try {
    const parsed = JSON.parse(commentStr);

    // 如果是数组格式
    if (Array.isArray(parsed)) {
      const items = parsed.map((item) => ({
        id: item.id || Date.now().toString(),
        content: item.content || "",
        author: item.author || "匿名用户",
        authorId: item.authorId,
        created_at: item.created_at || new Date().toISOString(),
        updatedAt: item.updatedAt,
        parentId: item.parentId,
        isEditing: false,
        isDeleted: false,
        isLiked: item.isLiked || false,
        likeCount: item.likeCount || 0,
        replies: item.replies
          ? item.replies.map((reply: any) => ({
              id: reply.id || Date.now().toString(),
              content: reply.content || "",
              author: reply.author || "匿名用户",
              authorId: reply.authorId,
              created_at: reply.created_at || new Date().toISOString(),
              updatedAt: reply.updatedAt,
              parentId: reply.parentId,
              isEditing: false,
              isDeleted: false,
              isLiked: reply.isLiked || false,
              likeCount: reply.likeCount || 0,
            }))
          : [],
      }));

      return {
        items,
        total: parsed.length,
        hasMore: false,
      };
    }

    // 如果是对象格式（包含 items 和 total）
    if (parsed.items && Array.isArray(parsed.items)) {
      const items = parsed.items.map((item: any) => ({
        id: item.id || Date.now().toString(),
        content: item.content || "",
        author: item.author || "匿名用户",
        authorId: item.authorId,
        created_at: item.created_at || new Date().toISOString(),
        updatedAt: item.updatedAt,
        parentId: item.parentId,
        isEditing: false,
        isDeleted: false,
        isLiked: item.isLiked || false,
        likeCount: item.likeCount || 0,
        replies: item.replies
          ? item.replies.map((reply: any) => ({
              id: reply.id || Date.now().toString(),
              content: reply.content || "",
              author: reply.author || "匿名用户",
              authorId: reply.authorId,
              created_at: reply.created_at || new Date().toISOString(),
              updatedAt: reply.updatedAt,
              parentId: reply.parentId,
              isEditing: false,
              isDeleted: false,
              isLiked: reply.isLiked || false,
              likeCount: reply.likeCount || 0,
            }))
          : [],
      }));

      return {
        items,
        total: parsed.total || parsed.items.length,
        hasMore: parsed.hasMore || false,
      };
    }

    // 如果是纯文本格式（兼容旧数据）
    if (typeof parsed === "string") {
      return {
        items: [
          {
            id: Date.now().toString(),
            content: parsed,
            author: "系统",
            created_at: new Date().toISOString(),
            isEditing: false,
            isDeleted: false,
            isLiked: false,
            likeCount: 0,
            replies: [],
          },
        ],
        total: 1,
        hasMore: false,
      };
    }
  } catch (error) {
    console.warn("Failed to parse comment string:", error);
    // 如果解析失败，尝试作为纯文本处理
    return {
      items: [
        {
          id: Date.now().toString(),
          content: commentStr,
          author: "系统",
          created_at: new Date().toISOString(),
          isEditing: false,
          isDeleted: false,
          isLiked: false,
          likeCount: 0,
          replies: [],
        },
      ],
      total: 1,
      hasMore: false,
    };
  }

  return {
    items: [],
    total: 0,
    hasMore: false,
  };
} // 工具函数：将前端结构转换为后端字符串
export function stringifyCommentThread(thread: CommentThread): string {
  try {
    const data = {
      items: thread.items.map((item) => ({
        id: item.id,
        content: item.content,
        author: item.author,
        authorId: item.authorId,
        created_at: item.created_at,
        updatedAt: item.updatedAt,
        parentId: item.parentId,
        isLiked: item.isLiked || false,
        likeCount: item.likeCount || 0,
        replies: item.replies
          ? item.replies.map((reply) => ({
              id: reply.id,
              content: reply.content,
              author: reply.author,
              authorId: reply.authorId,
              created_at: reply.created_at,
              updatedAt: reply.updatedAt,
              parentId: reply.parentId,
              isLiked: reply.isLiked || false,
              likeCount: reply.likeCount || 0,
            }))
          : [],
      })),
      total: thread.total,
      hasMore: thread.hasMore || false,
    };

    return JSON.stringify(data);
  } catch (error) {
    console.error("Failed to stringify comment thread:", error);
    return "";
  }
}

// 工具函数：创建新的评论项
export function createCommentItem(
  content: string,
  author: string,
  authorId?: number,
  parentId?: string
): CommentItem {
  return {
    id: `comment_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    content,
    author,
    authorId,
    created_at: new Date().toISOString(),
    parentId,
    isEditing: false,
    isDeleted: false,
  };
}

// 工具函数：添加评论到线程
export function addCommentToThread(
  thread: CommentThread,
  comment: CommentItem
): CommentThread {
  // 如果是回复评论，需要添加到对应的父评论下
  if (comment.parentId) {
    const updatedItems = thread.items.map((item) => {
      if (item.id === comment.parentId) {
        return {
          ...item,
          replies: [comment, ...(item.replies || [])], // 回复添加到父评论的 replies 数组中
        };
      }
      return item;
    });

    return {
      ...thread,
      items: updatedItems,
      total: thread.total + 1,
    };
  }

  // 如果是顶级评论，添加到顶部
  return {
    ...thread,
    items: [comment, ...thread.items],
    total: thread.total + 1,
  };
}

// 工具函数：更新线程中的评论
export function updateCommentInThread(
  thread: CommentThread,
  commentId: string,
  updates: Partial<CommentItem>
): CommentThread {
  return {
    ...thread,
    items: thread.items.map((item) =>
      item.id === commentId ? { ...item, ...updates } : item
    ),
  };
}

// 工具函数：从线程中删除评论
export function removeCommentFromThread(
  thread: CommentThread,
  commentId: string
): CommentThread {
  return {
    ...thread,
    items: thread.items.filter((item) => item.id !== commentId),
    total: Math.max(0, thread.total - 1),
  };
}
