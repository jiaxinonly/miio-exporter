from flask import Flask, Response, jsonify
from prometheus_client import generate_latest
from lib.tools import (
    load_config_and_devices,
    create_metrics_registry,
    update_metrics_from_device_data
)
from lib.logger import logger

app = Flask(__name__)

# 加载配置
config, devices_config, devices_list = load_config_and_devices()

# 初始化 Prometheus 指标
registry, metrics_list = create_metrics_registry(config)


@app.route('/metrics')
def metrics():
    for device in devices_list:
        device_config = devices_config.get(device.model, {})
        update_metrics_from_device_data(metrics_list, device, device_config)

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
    global config, devices_config, devices_list
    config, devices_config, devices_list = load_config_and_devices()

    # 初始化 Prometheus 指标
    global registry, metrics_list
    registry, metrics_list = create_metrics_registry(config)
    return jsonify({"message": "重新加载配置和设备列表成功"})


if __name__ == '__main__':
    app.run()
