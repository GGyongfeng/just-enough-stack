# 数据库迁移指南

本项目使用 Alembic 进行数据库迁移管理。

## 快速开始

### 1. 初始化迁移

如果这是第一次设置迁移，需要标记当前数据库状态：

```bash
uv run migrate.py init
```

### 2. 生成迁移文件

当你修改了 ORM 模型后，生成新的迁移文件：

```bash
uv run migrate.py migrate "迁移描述信息"
```

### 3. 运行迁移

应用所有待处理的迁移：

```bash
uv run migrate.py upgrade
```

### 4. 查看迁移状态

```bash
# 查看当前版本
uv run migrate.py current

# 查看迁移历史
uv run migrate.py history
```

### 5. 回滚迁移

```bash
uv run migrate.py downgrade <版本号>
```

## 原生 Alembic 命令

你也可以直接使用 Alembic 命令：

```bash
# 生成迁移
alembic revision --autogenerate -m "迁移描述"

# 运行迁移
alembic upgrade head

# 查看当前版本
alembic current

# 查看历史
alembic history

# 回滚
alembic downgrade <版本>
```

## 注意事项

1. 修改 ORM 模型后，务必生成对应的迁移文件
2. 在生产环境部署前，先在测试环境验证迁移
3. 备份重要数据库后再执行迁移
4. 迁移文件会自动检测数据库 URL（支持环境变量 `DATABASE_URL`）
