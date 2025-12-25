import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { visualizer } from "rollup-plugin-visualizer";
import fs from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface PackageJson {
  version?: string;
  description?: string;
  [key: string]: any;
}

interface VersionInfo {
  version: string;
  buildTime: string;
  description: string;
  buildEnv: string;
}

// 自动生成版本文件的插件
function generateVersionPlugin() {
  return {
    name: "generate-version",
    buildStart() {
      try {
        // 读取 package.json 获取版本号
        const packageJsonPath = resolve(process.cwd(), "package.json");
        const packageJson: PackageJson = JSON.parse(
          fs.readFileSync(packageJsonPath, "utf-8")
        );

        // 生成版本信息
        const versionInfo: VersionInfo = {
          version: packageJson.version || "1.0.0",
          buildTime: new Date().toISOString(),
          description: packageJson.description || "AgentEvalPlatform Frontend",
          buildEnv: process.env.NODE_ENV || "production",
        };

        // 写入版本文件到 public 目录
        const versionFilePath = resolve(process.cwd(), "public/version.json");
        fs.writeFileSync(versionFilePath, JSON.stringify(versionInfo, null, 2));

        console.log("✅ 版本文件已生成:", versionInfo);
      } catch (error) {
        console.error("❌ 生成版本文件失败:", error);
      }
    },
  };
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  console.log("------------vite.config.ts--------------");
  console.log("构建信息:");
  console.log("当前模式:", mode);
  console.log("当前工作目录:", process.cwd());
  console.log("环境变量:");
  console.log("- VITE_APP_TITLE:", env.VITE_APP_TITLE);
  console.log("- VITE_APP_VERSION:", env.VITE_APP_VERSION);

  return {
    plugins: [
      vue(),
      generateVersionPlugin(), // 自动生成版本文件
      visualizer({
        open: false,
        gzipSize: true, // 显示 gzip 大小
        brotliSize: true, // 显示 brotli 大小
        filename: "stats.html",
      }),
    ],

    esbuild: {
      drop: mode === "production" ? ["console", "debugger"] : [], // 生产环境移除
    },

    resolve: {
      alias: {
        "@": resolve(__dirname, "src"),
      },
      extensions: [".vue", ".ts", ".js"],
    },

    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @use "@/assets/styles/variables.scss";
          `,
        },
      },
    },

    server: {
      port: Number(env.VITE_PORT) || 3000,
      host: true,
      proxy: {
        "/api": {
          target: env.VITE_BASE_API_URL || "http://localhost:8080",
          changeOrigin: true,
        },
      },
    },

    build: {
      outDir: "dist",
      assetsDir: "assets",
      sourcemap: false,
      open: false,
      rollupOptions: {
        output: {
          assetFileNames: "assets/[name].[hash].[ext]",
          chunkFileNames: "assets/[name].[hash].js",
          entryFileNames: "assets/[name].[hash].js",
        },
      },
    },
  };
});
