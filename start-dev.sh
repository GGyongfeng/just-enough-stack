#!/bin/bash

PROJECT_DIR="$(pwd)"

echo "🚀 Just Enough Stack - 启动中..."
echo ""

# Check and install backend dependencies
if [ ! -d "$PROJECT_DIR/app/.venv" ]; then
  echo "📦 Installing backend dependencies..."
  cd "$PROJECT_DIR/app" && uv sync
fi

# Check and install frontend dependencies
if [ ! -d "$PROJECT_DIR/web/node_modules" ]; then
  echo "📦 Installing frontend dependencies..."
  cd "$PROJECT_DIR/web" && npm install
fi

echo ""
echo "✨ Starting services in separate terminal windows..."
echo ""

# Start backend in background
echo "🔧 Starting backend..."
osascript -e 'tell application "Terminal" to do script "cd '"$PROJECT_DIR"'/app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"'

# Wait a moment
sleep 2

# Start frontend in new terminal
echo "🎨 Starting frontend..."
osascript -e 'tell application "Terminal" to do script "cd '"$PROJECT_DIR"'/web && npm run dev"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 服务启动完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 访问地址："
echo "  - 前端：      http://localhost:3000"
echo "  - 后端 API：  http://localhost:8000"
echo "  - API 文档：  http://localhost:8000/docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
