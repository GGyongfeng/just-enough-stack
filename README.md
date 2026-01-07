# Just Enough Stack

**轻量级全栈开发框架** - 快速搭建微小型应用的脚手架

基于 **FastAPI + Vue3 + SQLite**，提供完整的用户认证、权限管理和 CRUD 示例。

## ⚡ 快速开始

### 克隆仓库
```bash
git clone https://github.com/GGyongfeng/just-enough-stack.git
cd just-enough-stack
```

### 一键启动

**macOS / Linux:**
```bash
./start-dev.sh
```

**Windows:**
```bash
start-dev.bat
```

脚本会自动：
- ✅ 检查依赖工具（Python, Node.js, npm, uv）
- ✅ 安装后端和前端依赖
- ✅ 启动后端和前端服务
- ✅ 自动打开浏览器访问 http://localhost:3000

### 环境要求
- Python 3.12+
- Node.js 18+
- npm 或 yarn
- [uv](https://astral.sh/uv) - Python 包管理工具

**安装 uv:**
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 技术栈

### 后端
- **FastAPI** - 现代化 Python Web 框架
- **SQLAlchemy** - ORM 数据库工具
- **Pydantic** - 数据验证与 API Schema（单一事实源 SSOT）
- **JWT** - 用户认证

### 前端
- **Vue3 + TypeScript** - 类型安全的前端框架
- **Vite** - 极速构建工具
- **Element Plus** - UI 组件库
- **Pinia** - 状态管理

## 核心功能

### 1. 用户认证与权限
- ✅ 注册/登录（JWT）
- ✅ RBAC 权限控制（Guest/User/Admin/Super Admin）
- ✅ 用户管理

### 2. CRUD 示例（任务管理）
- ✅ 创建、查看、更新、删除
- ✅ 状态跟踪（待处理/进行中/已完成/已取消）
- ✅ 优先级管理（低/中/高）
- ✅ 分页、筛选

### 3. 开发者友好
- ✅ RESTful API 设计
- ✅ 自动 API 文档（Swagger）
- 🚧 OpenAPI → TypeScript 类型自动生成（重构后）

### 手动启动（可选）

如果不使用启动脚本，可以分别启动：

**后端：**
```bash
cd app
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd web
npm install
npm run dev
```

### 访问地址
- 🌐 前端: http://localhost:3000
- 🔌 后端 API: http://localhost:8000
- 📚 API 文档: http://localhost:8000/docs

## 当前结构
```
just-enough-stack/
├── backend/          # FastAPI 后端
│   ├── src/
│   │   ├── api/v1/  # API 端点
│   │   ├── dao/     # 数据访问
│   │   ├── orm/     # 数据模型
│   │   └── types/   # Pydantic schemas
│   └── main.py
├── frontend/         # Vue3 前端
│   └── src/
│       ├── api/     # API 客户端
│       ├── stores/  # 状态管理
│       └── views/   # 页面组件
└── README.md
```

## 即将到来 🚀

**新项目结构（重构中）：**
```
je-stack/
├── je_stack/        # ✨ 可复用核心框架
│   ├── auth/       # 认证模块
│   ├── crud/       # CRUD 基类
│   ├── schemas/    # Pydantic（单一事实源 SSOT）
│   └── utils/
├── app/             # ✨ 示例应用
│   ├── api/
│   ├── models/
│   └── main.py
├── web/             # ✨ 前端
│   ├── src/
│   │   ├── api/types.ts  # 🔥 从 OpenAPI 自动生成
│   │   └── ...
│   └── package.json
├── scripts/
│   └── generate-types.sh  # 类型生成脚本
└── pyproject.toml
```

**核心改进：**
- ✅ 后端 Pydantic Schema 作为"单一事实源"
- ✅ 前端类型自动生成（`openapi-typescript`）
- ✅ 核心框架可独立复用
- ✅ 示例应用清晰分离

## API 响应格式
```json
{
  "success": true,
  "message": "操作成功",
  "data": { /* 业务数据 */ }
}
```

## 开发指南

### 添加新功能（当前）
1. 后端：定义 ORM → DAO → Pydantic Schema → API 端点
2. 前端：手写 TypeScript 类型 → API 客户端 → Store → 页面

### 添加新功能（重构后）
1. 后端：定义 Pydantic Schema → 其他同上
2. 前端：运行 `npm run generate-types` → 直接使用生成的类型

### 权限控制
```python
from src.middleware.auth import check_user_permission

@router.post("/tasks")
async def create_task(
    current_user = Depends(check_user_permission())
):
    pass  # 仅登录用户可访问
```

## 数据库
首次启动自动创建表。如需重置：
```bash
rm backend/app.db
```

## 路线图
- [x] 基础认证与权限系统
- [x] Task CRUD 示例
- [ ] 重构为 `je_stack` + `app` + `web`
- [ ] OpenAPI 类型自动生成
- [ ] Docker Compose
- [ ] 单元测试
- [ ] CI/CD

## 许可证
MIT License

## 贡献
欢迎 [Issues](../../issues) 和 [PRs](../../pulls)！

---
**Just Enough Stack** - 不多不少，刚刚好 🚀
