from flask import Flask, Response
from prometheus_client import generate_latest
from lib.tools import (
    load_config,
    create_metrics_registry,
    get_cloud_devices,
    update_metrics_from_device_data
)

app = Flask(__name__)

# 加载配置
config = load_config('config.yaml')
username = config.get("username", "")
password = config.get("password", "")
include = config.get("include", [])
exclude = config.get("exclude", [])
devices_config = config.get('devices', {})

# 初始化 Prometheus 指标
registry, metrics_list = create_metrics_registry(config)


@app.route('/metrics')
def metrics():
    # 动态查询设备列表
    devices_list = get_cloud_devices(username, password, include=include, exclude=exclude)
    for device in devices_list:
        device_config = devices_config.get(device.model, {})
        update_metrics_from_device_data(metrics_list, device, device_config)

    # 生成 Prometheus 格式的文本数据
    text = generate_latest(registry)
    return Response(text, status=200, mimetype='text/plain')


@app.route('/-/health')
def health():
    return {'message': 'miio-exporter is running!'}


if __name__ == '__main__':
    app.run()
