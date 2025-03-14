# 使用官方的 Python 运行时作为父镜像
FROM python:3.13

# 设置工作目录为 /app
WORKDIR /usr/local/miio-exporter

# 将本地代码复制到容器中的工作目录
COPY app.py requirements.txt /usr/local/miio-exporter/
COPY lib /usr/local/miio-exporter/lib

# 安装 requirements.txt 中指定的任何所需包
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple & pip install -r requirements.txt

# 使端口 9999 可供此容器外的世界访问
EXPOSE 9999

# 在容器启动时运行 app.py，并指定外部挂载的配置文件路径
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9999"]ls