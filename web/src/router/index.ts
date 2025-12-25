import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";
import BasicLayout from "@/layouts/BasicLayout.vue";

import { ROUTES } from "./routes";

// 路由守卫：检查认证状态
const requireAuth = (_to: any, _from: any, next: any) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    next();
  } else {
    next(ROUTES.AUTH.LOGIN);
  }
};

// 定义路由配置
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/tasks",
  },
  // 用户认证相关路由
  {
    path: ROUTES.AUTH.LOGIN,
    name: "Login",
    component: () => import("@/views/user/login.vue"),
    meta: { title: "用户登录" },
  },
  {
    path: ROUTES.AUTH.REGISTER,
    name: "Register",
    component: () => import("@/views/user/register.vue"),
    meta: { title: "用户注册" },
  },
  // 主页
  {
    path: ROUTES.DASHBOARD,
    component: BasicLayout,
    beforeEnter: requireAuth,
    children: [
      {
        path: "",
        name: "Dashboard",
        component: () => import("@/views/home/index.vue"),
        meta: { title: "首页" },
      },
    ],
  },
  // 任务管理
  {
    path: "/tasks",
    component: BasicLayout,
    beforeEnter: requireAuth,
    children: [
      {
        path: "",
        name: "TaskList",
        component: () => import("@/views/task/index.vue"),
        meta: { title: "任务管理" },
      },
      {
        path: ":id",
        name: "TaskDetail",
        component: () => import("@/views/task/detail.vue"),
        meta: {
          title: "任务详情",
          breadcrumb: [
            { text: "任务管理", to: { name: "TaskList" } },
            { text: "任务详情" },
          ],
        },
      },
    ],
  },
  // 个人资料
  {
    path: ROUTES.PROFILE,
    component: BasicLayout,
    beforeEnter: requireAuth,
    children: [
      {
        path: "",
        name: "UserProfile",
        component: () => import("@/views/user/profile.vue"),
        meta: { title: "个人中心" },
      },
    ],
  },
  // 错误页面
  {
    path: ROUTES.NOT_FOUND,
    component: BasicLayout,
    children: [
      {
        path: "",
        name: "NotFound",
        component: () => import("@/views/error/404.vue"),
        meta: { title: "页面未找到" },
      },
    ],
  },
  // 成功页面
  {
    path: "/success",
    name: "Success",
    component: () => import("@/views/success/index.vue"),
    meta: { title: "操作结果" },
  },
  // 通配符路由，必须放在最后
  {
    path: "/:pathMatch(.*)*",
    redirect: ROUTES.NOT_FOUND,
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 全局路由守卫
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  if (to.meta?.title) {
    document.title = `${to.meta.title} - Just Enough Stack`;
  }
  next();
});

// 重新导出 ROUTES 以保持向后兼容性
export { ROUTES } from "./routes";

export default router;
