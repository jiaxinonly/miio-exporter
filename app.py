from flask import Flask, Response
from prometheus_client import generate_latest
from lib.tools import DeviceData, get_cloud_device, Config

# 创建 Flask 应用
app = Flask(__name__)

devices_list = get_cloud_device()


@app.route('/metrics')
def metrics():

    for device in devices_list:
        DeviceData.create_metrics_data(device)

    # 生成 Prometheus 格式的文本数据
    text = generate_latest(Config.registry)
    return Response(text, status=200, mimetype='text/plain')


@app.route('/-/health')
def health():
    return {'message': 'miio-exporter is running!'}


if __name__ == '__main__':
    app.run()
