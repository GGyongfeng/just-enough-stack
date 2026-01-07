#!/bin/bash

set -e  # 遇到错误立即退出

PROJECT_DIR="$(pwd)"
FRONTEND_URL="http://localhost:3000"
BACKEND_URL="http://localhost:8000"

echo "🚀 Just Enough Stack - 启动中..."
echo ""

# ============================================
# 1. 检查必需的命令行工具
# ============================================
echo "🔍 检查依赖工具..."

check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo "❌ 错误: 未找到 $1"
    echo "   请安装 $1: $2"
    exit 1
  else
    echo "✅ $1 已安装: $($1 --version 2>&1 | head -n 1)"
  fi
}

check_command "python3" "https://www.python.org/downloads/"
check_command "node" "https://nodejs.org/"
check_command "npm" "https://nodejs.org/"
check_command "uv" "curl -LsSf https://astral.sh/uv/install.sh | sh"

echo ""

# ============================================
# 2. 检查并创建前端环境变量文件
# ============================================
if [ ! -f "$PROJECT_DIR/web/.env" ]; then
  echo "⚙️  创建前端环境变量文件..."
  cp "$PROJECT_DIR/web/.env.example" "$PROJECT_DIR/web/.env"
  echo "✅ 已从 .env.example 创建 .env"
  echo ""
fi

# ============================================
# 3. 安装依赖
# ============================================
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

# ============================================
# 4. 启动服务
# ============================================
# 检测操作系统
OS="$(uname -s)"

if [ "$OS" = "Darwin" ]; then
  # macOS - 使用 osascript
  osascript -e 'tell application "Terminal" to do script "cd '"$PROJECT_DIR"'/app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"' > /dev/null 2>&1

  osascript -e 'tell application "Terminal" to do script "cd '"$PROJECT_DIR"'/web && npm run dev"' > /dev/null 2>&1

  open "$FRONTEND_URL"

elif [ "$OS" = "Linux" ]; then
  # Linux - 使用 gnome-terminal 或 xterm
  if command -v gnome-terminal &> /dev/null; then
    echo "🔧 Starting backend..."
    gnome-terminal -- bash -c "cd '$PROJECT_DIR/app' && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash"

    echo "🎨 Starting frontend..."
    gnome-terminal -- bash -c "cd '$PROJECT_DIR/web' && npm run dev; exec bash"

    # 尝试打开浏览器
    if command -v xdg-open &> /dev/null; then
      xdg-open "$FRONTEND_URL"
    fi
  else
    echo "⚠️  请手动启动服务："
    echo "   终端1: cd app && uv run uvicorn main:app --reload"
    echo "   终端2: cd web && npm run dev"
  fi
else
  echo "⚠️  未识别的操作系统，请手动启动服务"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 服务启动完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 访问地址："
echo "  - 前端：      $FRONTEND_URL"
echo "  - 后端 API：  $BACKEND_URL"
echo "  - API 文档：  $BACKEND_URL/docs"
echo ""
echo "💡 提示："
echo "  - 前端会自动在浏览器中打开"
echo "  - 如未自动打开，请手动访问: $FRONTEND_URL"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
