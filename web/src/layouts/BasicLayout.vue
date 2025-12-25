<template>
  <div class="admin-layout-simple">
    <div :class="['sidebar-simple', { collapsed: isCollapsed }]">
      <div class="sidebar-header">
        <img src="/logo-暗岩灰.png" alt="Logo" class="logo" />
        <div class="collapse-btn-container" @click="toggleSidebar">
          <el-icon class="collapse-btn">
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              data-rtl-flip=""
              class="icon"
            >
              <path
                d="M6.83496 3.99992C6.38353 4.00411 6.01421 4.0122 5.69824 4.03801C5.31232 4.06954 5.03904 4.12266 4.82227 4.20012L4.62207 4.28606C4.18264 4.50996 3.81498 4.85035 3.55859 5.26848L3.45605 5.45207C3.33013 5.69922 3.25006 6.01354 3.20801 6.52824C3.16533 7.05065 3.16504 7.71885 3.16504 8.66301V11.3271C3.16504 12.2712 3.16533 12.9394 3.20801 13.4618C3.25006 13.9766 3.33013 14.2909 3.45605 14.538L3.55859 14.7216C3.81498 15.1397 4.18266 15.4801 4.62207 15.704L4.82227 15.79C5.03904 15.8674 5.31234 15.9205 5.69824 15.9521C6.01398 15.9779 6.383 15.986 6.83398 15.9902L6.83496 3.99992ZM18.165 11.3271C18.165 12.2493 18.1653 12.9811 18.1172 13.5702C18.0745 14.0924 17.9916 14.5472 17.8125 14.9648L17.7295 15.1415C17.394 15.8 16.8834 16.3511 16.2568 16.7353L15.9814 16.8896C15.5157 17.1268 15.0069 17.2285 14.4102 17.2773C13.821 17.3254 13.0893 17.3251 12.167 17.3251H7.83301C6.91071 17.3251 6.17898 17.3254 5.58984 17.2773C5.06757 17.2346 4.61294 17.1508 4.19531 16.9716L4.01855 16.8896C3.36014 16.5541 2.80898 16.0434 2.4248 15.4169L2.27051 15.1415C2.03328 14.6758 1.93158 14.167 1.88281 13.5702C1.83468 12.9811 1.83496 12.2493 1.83496 11.3271V8.66301C1.83496 7.74072 1.83468 7.00898 1.88281 6.41985C1.93157 5.82309 2.03329 5.31432 2.27051 4.84856L2.4248 4.57317C2.80898 3.94666 3.36012 3.436 4.01855 3.10051L4.19531 3.0175C4.61285 2.83843 5.06771 2.75548 5.58984 2.71281C6.17898 2.66468 6.91071 2.66496 7.83301 2.66496H12.167C13.0893 2.66496 13.821 2.66468 14.4102 2.71281C15.0069 2.76157 15.5157 2.86329 15.9814 3.10051L16.2568 3.25481C16.8833 3.63898 17.394 4.19012 17.7295 4.84856L17.8125 5.02531C17.9916 5.44285 18.0745 5.89771 18.1172 6.41985C18.1653 7.00898 18.165 7.74072 18.165 8.66301V11.3271ZM8.16406 15.995H12.167C13.1112 15.995 13.7794 15.9947 14.3018 15.9521C14.8164 15.91 15.1308 15.8299 15.3779 15.704L15.5615 15.6015C15.9797 15.3451 16.32 14.9774 16.5439 14.538L16.6299 14.3378C16.7074 14.121 16.7605 13.8478 16.792 13.4618C16.8347 12.9394 16.835 12.2712 16.835 11.3271V8.66301C16.835 7.71885 16.8347 7.05065 16.792 6.52824C16.7605 6.14232 16.7073 5.86904 16.6299 5.65227L16.5439 5.45207C16.32 5.01264 15.9796 4.64498 15.5615 4.3886L15.3779 4.28606C15.1308 4.16013 14.8165 4.08006 14.3018 4.03801C13.7794 3.99533 13.1112 3.99504 12.167 3.99504H8.16406C8.16407 3.99667 8.16504 3.99829 8.16504 3.99992L8.16406 15.995Z"
              ></path></svg
          ></el-icon>
        </div>
      </div>

      <ul>
        <template v-for="item in menuItems" :key="item.key">
          <!-- 分组类型 -->
          <li v-if="item.type === 'group'" class="menu-group">
            <div class="group-header">
              <span class="group-label">
                {{ isCollapsed ? item.collapsedLabel || "-" : item.label }}
              </span>
            </div>
            <!-- 分组子项 -->
            <template v-if="item.children">
              <li
                v-for="child in item.children"
                :key="child.key"
                :class="{ 'bottom-item': child.key === 'profile' }"
                class="group-child"
              >
                <!-- 外部链接 -->
                <el-tooltip
                  v-if="child.path && child.path.startsWith('http')"
                  :content="child.label"
                  placement="right"
                  :disabled="!isCollapsed"
                >
                  <a :href="child.path" target="_blank" class="menu-link external-link">
                    <el-icon v-if="child.icon" class="menu-icon">
                      <component :is="icons[child.icon]" />
                    </el-icon>
                    <span class="menu-text">{{ child.label }}</span>
                  </a>
                </el-tooltip>
                <!-- 内部路由 -->
                <el-tooltip
                  v-else-if="child.path"
                  :content="child.label"
                  placement="right"
                  :disabled="!isCollapsed"
                >
                  <router-link
                    :to="child.path"
                    :class="{ active: isActivePath(child.path) }"
                    class="menu-link"
                  >
                    <el-icon v-if="child.icon" class="menu-icon">
                      <component :is="icons[child.icon]" />
                    </el-icon>
                    <span class="menu-text">{{ child.label }}</span>
                  </router-link>
                </el-tooltip>
              </li>
            </template>
          </li>
          <!-- 普通菜单项 -->
          <li v-else :class="{ 'bottom-item': item.key === 'profile' }">
            <!-- 外部链接 -->
            <el-tooltip
              v-if="item.path && item.path.startsWith('http')"
              :content="item.label"
              placement="right"
              :disabled="!isCollapsed"
            >
              <a :href="item.path" target="_blank" class="menu-link external-link">
                <el-icon v-if="item.icon" class="menu-icon">
                  <component :is="icons[item.icon]" />
                </el-icon>
                <span class="menu-text">{{ item.label }}</span>
              </a>
            </el-tooltip>
            <!-- 内部路由 -->
            <el-tooltip
              v-else-if="item.path"
              :content="item.label"
              placement="right"
              :disabled="!isCollapsed"
            >
              <router-link
                :to="item.path"
                :class="{ active: isActivePath(item.path) }"
                class="menu-link"
              >
                <el-icon v-if="item.icon" class="menu-icon">
                  <component :is="icons[item.icon]" />
                </el-icon>
                <span class="menu-text">{{ item.label }}</span>
              </router-link>
            </el-tooltip>
          </li>
        </template>
      </ul>
    </div>
    <div class="main-content-simple">
      <div class="breadcrumb-container">
        <el-icon class="back-btn" @click="goBack">
          <Back />
        </el-icon>
        <div class="breadcrumb-content">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item
              v-for="(item, index) in breadcrumbItems"
              :key="index"
              :to="item.to"
            >
              <a v-if="item.path && !item.to" :href="item.path">{{ item.label }}</a>
              <span v-else>{{ item.label }}</span>
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts" setup>

import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { MENU_ITEMS, type MenuItem } from '@/router/menu'
import { Back } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()
const isCollapsed = computed({
  get: () => userStore.settings.sidebarCollapsed,
  set: (value: boolean) => userStore.updateSettings({ sidebarCollapsed: value })
})

const goBack = () => {
  router.back()
}

// 从菜单配置中自动提取所有图标名称
const getAllIconsFromMenu = (menuItems: MenuItem[]): string[] => {
  const iconSet = new Set<string>()

  const extractIcons = (items: MenuItem[]) => {
    items.forEach(item => {
      if (item.icon) iconSet.add(item.icon)
      if (item.children) extractIcons(item.children)
    })
  }

  extractIcons(menuItems)
  return Array.from(iconSet)
}

// 自动生成图标映射
const createIconMapping = (): Record<string, string> => {
  const iconNames = getAllIconsFromMenu(MENU_ITEMS)

  const mapping: Record<string, string> = {}
  iconNames.forEach(iconName => {
    mapping[iconName] = iconName
  })

  return mapping
}

const icons = createIconMapping()

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}


const route = useRoute()

// 使用简化的菜单项
const menuItems = computed<MenuItem[]>(() => {
  return MENU_ITEMS
})

// 面包屑根据路由meta中的breadcrumb配置渲染
const breadcrumbItems = computed(() => {
  const currentRoute = route.matched[route.matched.length - 1]

  // 如果路由meta中有breadcrumb配置，使用它
  if (currentRoute?.meta?.breadcrumb && Array.isArray(currentRoute.meta.breadcrumb)) {
    return currentRoute.meta.breadcrumb.map((item: any) => ({
      label: item.text,
      to: item.to || undefined,
      path: item.path || undefined
    }))
  }

  // 否则fallback到显示当前页面标题
  return currentRoute?.meta?.title ? [{ label: currentRoute.meta.title as string, to: undefined, path: undefined }] : []
})

const isActivePath = (path: string): boolean => {
  if (!path) return false

  const currentPath = route.path
  // 404页面：不高亮任何菜单
  if (currentPath === '/404') return false

  // 特殊处理：评估统计菜单在评估统计相关页面都应该高亮
  if (path === '/offline-data' && (
    currentPath.startsWith('/offline-data') ||
    currentPath.startsWith('/query/') ||
    currentPath.startsWith('/agent/')
  )) return true

  // 特殊处理：任务管理菜单在任务相关页面都应该高亮
  if (path === '/tasks' && currentPath.startsWith('/tasks')) return true

  // 默认：精确匹配或路径前缀匹配（用于子路由）
  if (path === currentPath) return true

  return false
}

console.log('BasicLayout loaded')
</script>

<style scoped>
.admin-layout-simple {
  display: flex;
  height: 100vh;
}

.sidebar-simple {
  width: 200px;
  padding: 20px 8px;
  background: var(--el-color-primary-light-card-bg);
  color: var(--el-text-color-primary);
  border-right: 1px solid var(--el-border-color-light);
  transition: width var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.sidebar-simple.collapsed {
  width: 57px;
  padding: 20px 8px;
}

/* Header 样式 */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
  position: relative;
  height: 30px;
  flex-shrink: 0; /* 防止被压缩 */
}

.sidebar-simple.collapsed .sidebar-header {
  justify-content: space-between;
}

.logo {
  height: 26px;
  width: 26px;
  border-radius: 4px;
  position: absolute;
  left: 7px;
}

.collapse-btn-container {
  cursor: w-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  position: absolute;
  right: 0px;
}

.collapse-btn-container:hover {
  background-color: var(--el-color-primary-light-4);
}

.collapse-btn {
  font-size: 25px;
  color: var(--el-text-color-primary);
}

.sidebar-simple.collapsed .collapse-btn-container {
  right: 0px;
  opacity: 0;
  cursor: e-resize;
}

.sidebar-simple.collapsed .sidebar-header:hover .collapse-btn-container {
  opacity: 1;
}

/* 菜单切换按钮样式 */
.menu-toggle-container {
  margin-bottom: 10px;
  flex-shrink: 0; /* 防止被压缩 */
}

.menu-toggle-wrapper {
  position: relative;
  background: var(--el-color-primary-light-3);
  border-radius: 4px;
  padding: 3px;
  display: flex;
  height: 36px;
  transition: all var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-toggle-wrapper.collapsed {
  padding: 0px;
}

.menu-toggle-slider {
  position: absolute;
  top: 3px;
  left: 3px;
  width: calc(50% - 3px);
  height: calc(100% - 6px);
  background: var(--el-color-primary-light-2);
  border-radius: 4px;
  transition: transform var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.menu-toggle-wrapper.collapsed .menu-toggle-slider {
  left: 2px;
  width: calc(50% - 2px);
}

.menu-toggle-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 4px;
  transition: color var(--el-transition-duration-fast) ease;
  position: relative;
  z-index: 2;
  color: var(--el-text-color-regular);
  overflow: hidden;
}

.menu-toggle-option.active {
  color: white;
}

/* 文字显示控制 */
.menu-toggle-option .full-text {
  display: block;
  transition: opacity var(--el-transition-duration-fast) ease;
}

.menu-toggle-option .short-text {
  display: none;
  transition: opacity var(--el-transition-duration-fast) ease;
}

.menu-toggle-wrapper.collapsed .menu-toggle-option .full-text {
  display: none;
}

.menu-toggle-wrapper.collapsed .menu-toggle-option .short-text {
  display: block;
  font-size: 11px;
}

/* 折叠状态下的单一选项样式 */
.menu-toggle-option.collapsed-single {
  width: 100%;
  background: var(--el-color-primary-light-2);
  color: white;
  font-weight: 500;
  border-radius: 4px;
}

/* 菜单列表样式 */
.sidebar-simple ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  flex: 1; /* 自动占据剩余空间 */
  overflow-y: auto;
  min-height: 0; /* 确保flex子项可以收缩 */
}

.sidebar-simple li {
  margin-bottom: 8px;
}

.sidebar-simple li.bottom-item {
  margin-top: auto;
  margin-bottom: 0;
}

/* 菜单链接样式 */
.menu-link {
  color: var(--el-text-color-primary);
  text-decoration: none;
  padding: 10px 10px;
  display: flex;
  align-items: center;
  border-radius: 6px;
  height: 40px;
  overflow: hidden;
}

.menu-link:hover {
  background-color: var(--el-color-primary-light-4);
}

.menu-link.active {
  background-color: var(--el-color-primary-light-3);
  font-weight: 500;
}

/* 菜单图标样式 - 固定位置 */
.menu-icon {
  width: 20px;
  height: 20px;
  font-size: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 菜单文字样式 - 关键改动在这里 */
.menu-text {
  margin-left: 12px;
  white-space: nowrap;
  transition: opacity var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1),
    transform var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1),
    width var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  transform-origin: left center;
}

/* 折叠状态下的文字动画 */
.sidebar-simple.collapsed .menu-text {
  opacity: 0;
  transform: translateX(-10px);
  width: 0;
  margin-left: 0;
}

/* 外部链接特殊样式 */
.menu-link.external-link {
  color: var(--el-text-color-primary);
}

.menu-link.external-link:hover {
  background-color: var(--el-color-primary-light-3);
}

/* 主内容区域 */
.main-content-simple {
  flex: 1;
  overflow-y: auto;
  transition: margin-left var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
}

.breadcrumb-container {
  position: sticky;
  top: 0;
  width: 100%;
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  z-index: 1000;
  display: flex;
  align-items: center;
}

.breadcrumb-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 0px;
}

.back-btn {
  font-size: 30px;
  padding: 5px;
  margin: 0px 10px;
  color: var(--el-text-color-regular);
  cursor: pointer;
  border-radius: 4px;
}

.back-btn:hover {
  color: var(--el-color-primary-light);
  background-color: var(--el-color-primary-light-4);
}

/* 分组样式 */
.menu-group {
  margin-bottom: 4px;
}

.group-header {
  padding: 4px 10px;
  margin-bottom: 4px;
}

.group-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--el-text-color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: opacity var(--el-transition-duration-fast) cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-simple.collapsed .group-label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 400;
  color: var(--el-text-color-regular);
}
</style>
