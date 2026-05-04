import os

from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# 启动应用时读取项目根目录中的 .env 文件。
# .env 适合在本地开发时保存数据库地址等配置。
load_dotenv()


# 创建 FastAPI 应用实例。
# app 是整个 Web 服务的入口，uvicorn 会加载这个变量来启动服务。
app = FastAPI()


# 从环境变量中读取 PostgreSQL 数据库连接字符串。
# 常见格式：
# postgresql://用户名:密码@数据库地址:5432/数据库名
DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_url() -> str | None:
    """把 DATABASE_URL 转换成 SQLAlchemy + Psycopg 3 推荐使用的格式。"""
    # 如果没有配置 DATABASE_URL，返回 None，表示暂时不连接数据库。
    if not DATABASE_URL:
        return None

    # SQLAlchemy 使用 Psycopg 3 时，推荐的协议前缀是 postgresql+psycopg://。
    # 但很多云数据库平台给出的连接字符串是 postgresql://，这里自动做兼容转换。
    if DATABASE_URL.startswith("postgresql://"):
        return DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

    # 如果用户已经写了 postgresql+psycopg://，或者使用其他 SQLAlchemy 支持的格式，
    # 就直接原样返回。
    return DATABASE_URL


def test_database_connection() -> bool:
    """测试数据库是否可以连接成功。"""
    database_url = get_database_url()

    # 如果没有配置 DATABASE_URL，直接返回 False。
    # 这样应用本身仍然可以启动，方便先学习 FastAPI 和接口测试。
    if not database_url:
        return False

    try:
        # create_engine 会根据连接字符串创建数据库连接引擎。
        # pool_pre_ping=True 会在复用连接前检查连接是否有效，适合后端服务使用。
        engine = create_engine(database_url, pool_pre_ping=True)

        # with 会在代码块结束后自动关闭连接，避免资源泄漏。
        with engine.connect() as connection:
            # SELECT 1 是最简单的数据库查询，常用于测试连接是否正常。
            connection.execute(text("SELECT 1"))

        return True
    except SQLAlchemyError:
        # 如果数据库地址、用户名、密码等配置错误，连接会失败。
        return False


@app.get("/")
def read_root():
    """最简单的首页接口。"""
    return {"message": "Hello World"}


@app.get("/db-check")
def db_check():
    """检查数据库连接是否正常的接口。"""
    is_connected = test_database_connection()
    return {"database_connected": is_connected}
