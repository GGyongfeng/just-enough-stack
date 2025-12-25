import { ROUTES } from "./routes";

// 菜单项接口
export interface MenuItem {
  key: string;
  label: string;
  path?: string;
  icon?: string;
  children?: MenuItem[];
  type?: "item" | "group";
  collapsedLabel?: string;
}

// 主菜单配置
// Element Plus icons: https://element-plus.org/en-US/component/icon.html
export const MENU_ITEMS: MenuItem[] = [
  {
    key: "dashboard",
    label: "首页",
    path: ROUTES.DASHBOARD,
    icon: "House",
  },
  {
    key: "tasks",
    label: "任务管理",
    path: ROUTES.TASKS,
    icon: "List",
  },
  {
    key: "profile",
    label: "个人中心",
    path: ROUTES.PROFILE,
    icon: "User",
  },
];
