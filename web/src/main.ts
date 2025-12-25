import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";
import router from "./router";
import "./assets/styles/main.scss";

import { createPinia } from "pinia";
import { useUserStore } from "./stores/user";
import { mittBus } from "./utils/sys";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

// 标题调用.env.VITE_APP_TITLE
document.title = import.meta.env.VITE_APP_TITLE || "My Vue App";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia); // Pinia 必须在 router 之前注册

// 初始化用户存储状态
const userStore = useUserStore();
userStore.initializeFromStorage();

app.use(router);
// 全局使用 Element Plus 组件
app.use(ElementPlus);

// 全局注册 Element Plus icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 添加全局快捷键监听 - command/ctrl + shift + f 触发烟花
window.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === "f") {
    e.preventDefault();
    mittBus.emit("triggerFireworks");
  }
});

app.mount("#app");
