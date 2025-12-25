/**
 * 时间格式化工具函数
 */

/**
 * 格式化日期时间
 * @param dateTime 日期时间字符串或时间戳
 * @param format 格式类型
 * @returns 格式化后的日期时间字符串
 */
export function formatDateTime(dateTime: string | number | Date, format: 'full' | 'date' | 'time' | 'datetime' = 'datetime'): string {
  if (!dateTime) return '-'

  const date = new Date(dateTime)

  if (isNaN(date.getTime())) {
    return '-'
  }

  const options: Intl.DateTimeFormatOptions = {
    timeZone: 'Asia/Shanghai'
  }

  switch (format) {
    case 'full':
      options.year = 'numeric'
      options.month = '2-digit'
      options.day = '2-digit'
      options.hour = '2-digit'
      options.minute = '2-digit'
      options.second = '2-digit'
      break
    case 'date':
      options.year = 'numeric'
      options.month = '2-digit'
      options.day = '2-digit'
      break
    case 'time':
      options.hour = '2-digit'
      options.minute = '2-digit'
      options.second = '2-digit'
      break
    case 'datetime':
    default:
      options.year = 'numeric'
      options.month = '2-digit'
      options.day = '2-digit'
      options.hour = '2-digit'
      options.minute = '2-digit'
      break
  }

  return date.toLocaleString('zh-CN', options)
}

/**
 * 截断文本
 * @param text 原始文本
 * @param length 最大长度
 * @param suffix 后缀
 * @returns 截断后的文本
 */
export function truncateText(text: string, length: number, suffix: string = '...'): string {
  if (!text || text.length <= length) {
    return text
  }
  return text.substring(0, length) + suffix
}

/**
 * 格式化持续时间
 * @param duration 持续时间（毫秒）
 * @returns 格式化后的持续时间字符串
 */
export function formatDuration(duration?: number | null): string {
  if (!duration) return '-'

  if (duration < 1000) return `${duration}ms`
  if (duration < 60000) return `${(duration / 1000).toFixed(1)}s`
  return `${(duration / 60000).toFixed(1)}min`
}

/**
 * 计算两个时间之间的持续时间
 * @param startTime 开始时间
 * @param endTime 结束时间
 * @returns 持续时间（毫秒）
 */
export function calculateDuration(startTime: string | Date, endTime?: string | Date | null): number | null {
  if (!endTime) return null

  const start = new Date(startTime).getTime()
  const end = new Date(endTime).getTime()

  if (isNaN(start) || isNaN(end)) return null

  return end - start
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @returns 格式化后的文件大小字符串
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'

  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

/**
 * 获取相对时间
 * @param dateTime 日期时间
 * @returns 相对时间字符串
 */
export function getRelativeTime(dateTime: string | number | Date): string {
  const date = new Date(dateTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return formatDateTime(date, 'date')
}