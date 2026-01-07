#!/usr/bin/env python3
"""
Just Enough Stack - 跨平台启动脚本
支持 Windows / macOS / Linux
"""

import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

# 配置
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"
PROJECT_DIR = Path(__file__).parent.absolute()


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50 + "\n")


def check_command(command, install_url):
    """检查命令是否存在"""
    try:
        if platform.system() == "Windows":
            subprocess.run(["where", command], check=True, capture_output=True)
        else:
            subprocess.run(
                ["command", "-v", command], check=True, capture_output=True, shell=True
            )

        # 获取版本信息
        try:
            result = subprocess.run(
                [command, "--version"], capture_output=True, text=True, timeout=3
            )
            version = (
                result.stdout.split("\n")[0]
                if result.stdout
                else result.stderr.split("\n")[0]
            )
            print(f"✅ {command} 已安装: {version}")
        except:
            print(f"✅ {command} 已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ 错误: 未找到 {command}")
        print(f"   请安装: {install_url}")
        return False


def check_dependencies():
    """检查所有依赖"""
    print("[1/4] 检查依赖工具...")

    checks = [
        (
            "python3" if platform.system() != "Windows" else "python",
            "https://www.python.org/downloads/",
        ),
        ("node", "https://nodejs.org/"),
        ("npm", "https://nodejs.org/"),
        ("uv", "https://astral.sh/uv"),
    ]

    all_ok = True
    for cmd, url in checks:
        if not check_command(cmd, url):
            all_ok = False

    if not all_ok:
        sys.exit(1)
    print()


def setup_env_file():
    """创建前端环境变量文件"""
    print("[2/4] 检查环境变量文件...")

    env_file = PROJECT_DIR / "web" / ".env"
    env_example = PROJECT_DIR / "web" / ".env.example"

    if not env_file.exists():
        print("⚙️  创建 web/.env 文件...")
        env_file.write_text(env_example.read_text())
        print("✅ 已从 .env.example 创建 .env")
    else:
        print("✅ web/.env 已存在")
    print()


def install_dependencies():
    """安装依赖"""
    print("[3/4] 检查并安装依赖...")

    # 后端依赖
    app_venv = PROJECT_DIR / "app" / ".venv"
    if not app_venv.exists():
        print("📦 安装后端依赖...")
        subprocess.run(["uv", "sync"], cwd=PROJECT_DIR / "app", check=True)
        print("✅ 后端依赖安装完成")
    else:
        print("✅ 后端依赖已安装")

    # 前端依赖
    node_modules = PROJECT_DIR / "web" / "node_modules"
    if not node_modules.exists():
        print("📦 安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=PROJECT_DIR / "web", check=True)
        print("✅ 前端依赖安装完成")
    else:
        print("✅ 前端依赖已安装")
    print()


def start_services():
    """启动服务"""
    print("[4/4] 启动服务...\n")

    system = platform.system()

    if system == "Windows":
        # Windows: 使用 start 命令打开新窗口
        print("🔧 启动后端服务...")
        subprocess.Popen(
            f'start "Backend" cmd /k "cd /d {PROJECT_DIR}\\app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"',
            shell=True,
        )

        print("🎨 启动前端服务...")
        subprocess.Popen(
            f'start "Frontend" cmd /k "cd /d {PROJECT_DIR}\\web && npm run dev"',
            shell=True,
        )

    elif system == "Darwin":
        # macOS: 使用 osascript 打开新终端
        print("🔧 启动后端服务...")
        subprocess.run(
            [
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd {PROJECT_DIR}/app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"',
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print("🎨 启动前端服务...")
        subprocess.run(
            [
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd {PROJECT_DIR}/web && npm run dev"',
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    else:
        # Linux: 尝试使用 gnome-terminal
        print("🔧 启动后端服务...")
        try:
            subprocess.Popen(
                [
                    "gnome-terminal",
                    "--",
                    "bash",
                    "-c",
                    f"cd {PROJECT_DIR}/app && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash",
                ]
            )

            print("🎨 启动前端服务...")
            subprocess.Popen(
                [
                    "gnome-terminal",
                    "--",
                    "bash",
                    "-c",
                    f"cd {PROJECT_DIR}/web && npm run dev; exec bash",
                ]
            )
        except FileNotFoundError:
            print("⚠️  未找到 gnome-terminal，请手动启动服务：")
            print(f"   终端1: cd {PROJECT_DIR}/app && uv run uvicorn main:app --reload")
            print(f"   终端2: cd {PROJECT_DIR}/web && npm run dev")
            return

    webbrowser.open(FRONTEND_URL)


def main():
    """主函数"""
    print_header("Just Enough Stack - 启动中...")

    try:
        check_dependencies()
        setup_env_file()
        install_dependencies()
        start_services()

        print_header("服务启动完成！")
        print("📍 访问地址：")
        print(f"  - 前端:      {FRONTEND_URL}")
        print(f"  - 后端 API:  {BACKEND_URL}")
        print(f"  - API 文档:  {BACKEND_URL}/docs")
        print()
        print("💡 提示：")
        print("  - 前端会自动在浏览器中打开")
        print("  - 后端和前端服务已在新窗口中启动")
        print("  - 按 Ctrl+C 可停止各个服务")
        print("\n" + "=" * 50 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  启动被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
