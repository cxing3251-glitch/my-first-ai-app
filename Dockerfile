# 使用 Python 3.13 slim 官方镜像作为基础环境。
FROM python:3.13-slim

# 设置容器内的工作目录。
WORKDIR /app

# 先复制依赖文件，方便 Docker 利用缓存加快后续构建。
COPY requirements.txt .

# 安装项目依赖。
RUN pip install --no-cache-dir -r requirements.txt

# 把当前项目中的代码复制到容器内。
COPY . .

# 声明容器会使用 8000 端口。
EXPOSE 8000

# 启动 FastAPI 应用。
# 0.0.0.0 表示允许容器外部访问服务。
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
