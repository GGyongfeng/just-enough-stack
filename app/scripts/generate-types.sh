#!/bin/bash

# OpenAPI TypeScript 类型自动生成脚本
# 使用 openapi-typescript 从后端 FastAPI 的 OpenAPI schema 生成前端类型

set -e

echo "🚀 生成 TypeScript 类型..."

# 确保后端服务正在运行
if ! curl -s http://localhost:8000/openapi.json > /dev/null; then
    echo "❌ 错误: 后端服务未运行！"
    echo "请先启动后端: cd app && uv run uvicorn main:app --reload"
    exit 1
fi

# 安装 openapi-typescript（如果未安装）
if ! command -v openapi-typescript &> /dev/null; then
    echo "📦 安装 openapi-typescript..."
    npm install -g openapi-typescript
fi

# 生成类型文件
echo "📝 从 http://localhost:8000/openapi.json 生成类型..."
npx openapi-typescript http://localhost:8000/openapi.json -o web/src/api/types.generated.ts

echo "✅ 类型生成完成！"
echo "📄 输出文件: web/src/api/types.generated.ts"
echo ""
echo "💡 提示: 现在可以在前端直接导入使用："
echo "   import type { components } from '@/api/types.generated'"
echo "   type TaskResponse = components['schemas']['TaskResponse']"
