#!/usr/bin/env python3
"""
数据库迁移管理脚本
"""
import os
import argparse
from alembic import command
from alembic.config import Config

def get_alembic_config():
    """获取Alembic配置"""
    config = Config("alembic.ini")
    database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
    config.set_main_option("sqlalchemy.url", database_url)
    return config

def init_migration():
    """初始化迁移（标记当前数据库状态）"""
    config = get_alembic_config()
    try:
        command.stamp(config, "head")
        print("✅ 数据库迁移已初始化，当前状态已标记")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    return True

def generate_migration(message: str):
    """生成新的迁移文件"""
    config = get_alembic_config()
    try:
        command.revision(config, autogenerate=True, message=message)
        print(f"✅ 迁移文件已生成: {message}")
    except Exception as e:
        print(f"❌ 生成迁移失败: {e}")
        return False
    return True

def run_migration():
    """运行迁移"""
    config = get_alembic_config()
    try:
        command.upgrade(config, "head")
        print("✅ 数据库迁移已完成")
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        return False
    return True

def show_history():
    """显示迁移历史"""
    config = get_alembic_config()
    try:
        command.history(config)
    except Exception as e:
        print(f"❌ 获取历史失败: {e}")

def show_current():
    """显示当前版本"""
    config = get_alembic_config()
    try:
        command.current(config)
    except Exception as e:
        print(f"❌ 获取当前版本失败: {e}")

def downgrade(revision: str):
    """回滚到指定版本"""
    config = get_alembic_config()
    try:
        command.downgrade(config, revision)
        print(f"✅ 已回滚到版本: {revision}")
    except Exception as e:
        print(f"❌ 回滚失败: {e}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="数据库迁移管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 初始化命令
    subparsers.add_parser("init", help="初始化迁移（标记当前数据库状态）")
    
    # 生成迁移命令
    migrate_parser = subparsers.add_parser("migrate", help="生成新的迁移文件")
    migrate_parser.add_argument("message", help="迁移描述信息")
    
    # 运行迁移命令
    subparsers.add_parser("upgrade", help="运行所有待处理的迁移")
    
    # 显示历史命令
    subparsers.add_parser("history", help="显示迁移历史")
    
    # 显示当前版本命令
    subparsers.add_parser("current", help="显示当前数据库版本")
    
    # 回滚命令
    downgrade_parser = subparsers.add_parser("downgrade", help="回滚到指定版本")
    downgrade_parser.add_argument("revision", help="目标版本")

    args = parser.parse_args()

    if args.command == "init":
        init_migration()
    elif args.command == "migrate":
        generate_migration(args.message)
    elif args.command == "upgrade":
        run_migration()
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()
    elif args.command == "downgrade":
        downgrade(args.revision)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()