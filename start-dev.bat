@echo off
setlocal enabledelayedexpansion

set FRONTEND_URL=http://localhost:3000
set BACKEND_URL=http://localhost:8000

echo.
echo ========================================
echo   Just Enough Stack - 启动中...
echo ========================================
echo.

REM ============================================
REM 1. 检查必需的命令行工具
REM ============================================
echo [1/4] 检查依赖工具...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Python
    echo 请安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已安装

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 Node.js
    echo 请安装 Node.js: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js 已安装

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 npm
    echo 请安装 Node.js (npm 会随 Node.js 一起安装)
    pause
    exit /b 1
)
echo [OK] npm 已安装

where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 未找到 uv
    echo 请安装 uv: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    pause
    exit /b 1
)
echo [OK] uv 已安装

echo.

REM ============================================
REM 2. 检查并创建前端环境变量文件
REM ============================================
echo [2/4] 检查环境变量文件...

if not exist "web\.env" (
    echo 创建 web\.env 文件...
    copy "web\.env.example" "web\.env" >nul
    echo [OK] 已从 .env.example 创建 .env
) else (
    echo [OK] web\.env 已存在
)

echo.

REM ============================================
REM 3. 安装依赖
REM ============================================
echo [3/4] 检查并安装依赖...

if not exist "app\.venv" (
    echo 安装后端依赖...
    cd app
    uv sync
    cd ..
    echo [OK] 后端依赖安装完成
) else (
    echo [OK] 后端依赖已安装
)

if not exist "web\node_modules" (
    echo 安装前端依赖...
    cd web
    call npm install
    cd ..
    echo [OK] 前端依赖安装完成
) else (
    echo [OK] 前端依赖已安装
)

echo.

REM ============================================
REM 4. 启动服务
REM ============================================
echo [4/4] 启动服务...

REM 启动后端（新窗口）
echo 启动后端服务...
start "Just Enough Stack - Backend" cmd /k "cd /d %cd%\app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

REM 启动前端（新窗口）
echo 启动前端服务...
start "Just Enough Stack - Frontend" cmd /k "cd /d %cd%\web && npm run dev"

REM 等待 3 秒
echo 等待服务启动...
timeout /t 3 /nobreak >nul

REM 打开浏览器
echo 打开浏览器...
start %FRONTEND_URL%

echo.
echo ========================================
echo   服务启动完成！
echo ========================================
echo.
echo 访问地址:
echo   - 前端:      %FRONTEND_URL%
echo   - 后端 API:  %BACKEND_URL%
echo   - API 文档:  %BACKEND_URL%/docs
echo.
echo 提示:
echo   - 前端和后端服务已在新窗口中启动
echo   - 浏览器会自动打开前端页面
echo   - 按 Ctrl+C 可停止各个服务
echo.
echo ========================================
echo.
pause
