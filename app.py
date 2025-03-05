# -*- coding: utf-8 -*-
# File: app.py
# Time: 2025/3/2 17:41
# Author: jiaxin
# Email: 1094630886@qq.com

from flask import Flask, Response, jsonify
from prometheus_client import generate_latest, push_to_gateway
from lib.tools import (
    load_config_and_devices,
    create_metrics_registry,
    update_metrics_from_device_data
)
from lib.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_client.exposition import basic_auth_handler

app = Flask(__name__)

# 加载配置
config = load_config_and_devices()

# 初始化 Prometheus 指标
registry, metrics_list = create_metrics_registry(config)

if config['push_mode']['active']:
    logger.info("启动推送模式")
    # 初始化定时任务调度器
    scheduler = BackgroundScheduler()
    scheduler.start()


@scheduler.scheduled_job('interval', seconds=config['push_mode']['interval'])
def push_metrics():
    logger.info("推送数据。。。")
    update_metrics_from_device_data(config, metrics_list)
    if config.get("push_mode").get("basic_auth"):
        push_to_gateway(config['push_mode']['pushgateway_url'], job=config['push_mode']['job_name'], registry=registry,
                        handler=lambda url, method, timeout, headers, data: basic_auth_handler(url, method, timeout,
                                                                                               headers, data,
                                                                                               config.get(
                                                                                                   "push_mode").get(
                                                                                                   "basic_auth").get(
                                                                                                   "username"),
                                                                                               config.get(
                                                                                                   "push_mode").get(
                                                                                                   "basic_auth").get(
                                                                                                   "password")))
    else:
        push_to_gateway(config['push_mode']['pushgateway_url'], job=config['push_mode']['job_name'],
                        registry=registry)
    logger.info("推送成功。。。")


@app.route('/metrics')
def metrics():
    update_metrics_from_device_data(config, metrics_list)
    # 生成 Prometheus 格式的文本数据
    text = generate_latest(registry)
    return Response(text, status=200, mimetype='text/plain')


@app.route('/-/health')
def health():
    return {'message': 'miio-exporter is running!'}


@app.route('/-/reload')
def reload():
    logger.info("重新加载配置和设备列表")

    # 加载配置
    global config
    config = load_config_and_devices()

    # 初始化 Prometheus 指标
    global registry, metrics_list
    registry, metrics_list = create_metrics_registry(config)
    return jsonify({"message": "重新加载配置和设备列表成功"})


if __name__ == '__main__':
    app.run()
