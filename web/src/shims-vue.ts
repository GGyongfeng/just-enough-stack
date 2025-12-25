// TypeScript 默认并不知道 .vue 文件是什么类型。如果没有这个声明文件，当你在 TypeScript 文件（如 router/index.ts）里 import 一个 .vue 文件时，TypeScript 会报“找不到模块”或“没有类型声明”的错误。
// 作用
// shims-vue.d.ts 文件告诉 TypeScript：
// “所有以 .vue 结尾的文件，都是一个 Vue 组件（DefineComponent 类型）。”

declare module '*.vue' {
    import { DefineComponent } from 'vue'
    const component: DefineComponent<{}, {}, any>
    export default component
  }