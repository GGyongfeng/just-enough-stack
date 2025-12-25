/**
 * 时间工具函数
 */

/**
 * 将时间戳转换为相对时间显示
 * @param timestamp 时间戳（毫秒）
 * @returns 相对时间字符串，如 "几秒前"、"几分钟前"、"几小时前"、"1天前"、"2024年1月2日"
 */
export function formatRelativeTime(timestamp: number): string {
  const now = Date.now();
  const diff = now - timestamp;
  
  // 如果时间戳大于当前时间（未来时间），返回具体日期
  if (diff < 0) {
    return new Date(timestamp).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) {
    return seconds <= 5 ? '刚刚' : `${seconds}秒前`;
  } else if (minutes < 60) {
    return `${minutes}分钟前`;
  } else if (hours < 24) {
    return `${hours}小时前`;
  } else if (days === 1) {
    return '1天前';
  } else if (days < 3) {
    return `${days}天前`;
  } else {
    // 超过3天显示具体日期
    return new Date(timestamp).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @returns 格式化后的文件大小字符串
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * 格式化持续时间（毫秒转换为可读格式）
 * @param milliseconds 毫秒数
 * @returns 格式化后的持续时间字符串
 */
export function formatDuration(milliseconds: number): string {
  const seconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) {
    return `${days}天${hours % 24}小时`;
  } else if (hours > 0) {
    return `${hours}小时${minutes % 60}分钟`;
  } else if (minutes > 0) {
    return `${minutes}分钟${seconds % 60}秒`;
  } else {
    return `${seconds}秒`;
  }
}

/**
 * 检查时间戳是否为今天
 * @param timestamp 时间戳（毫秒）
 * @returns 是否为今天
 */
export function isToday(timestamp: number): boolean {
  const today = new Date();
  const date = new Date(timestamp);
  
  return today.getFullYear() === date.getFullYear() &&
         today.getMonth() === date.getMonth() &&
         today.getDate() === date.getDate();
}

/**
 * 检查时间戳是否为昨天
 * @param timestamp 时间戳（毫秒）
 * @returns 是否为昨天
 */
export function isYesterday(timestamp: number): boolean {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const date = new Date(timestamp);
  
  return yesterday.getFullYear() === date.getFullYear() &&
         yesterday.getMonth() === date.getMonth() &&
         yesterday.getDate() === date.getDate();
}