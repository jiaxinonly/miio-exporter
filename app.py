from flask import Flask, Response
from miio.cloud import CloudInterface
from miio.chuangmi_plug import ChuangmiPlug
from miio.device import Device
import re
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from lib.tools import DeviceData
from yaml import safe_load



with open('config.yaml', 'r') as f:
    config = safe_load(f)
    print(config)
    username = config.get("username")
    password = config.get("password")
    print(username, password)

    exclude = ['热水器', '米家纯净式智能加湿器 2 lite', '米家直流变频两季扇', '空调插座', '温湿度传感器2', '温湿度传感器']
    devices_list = []

app = Flask(__name__)




def get_cloud_device():
    cloud = CloudInterface(username, password)
    devices = cloud.get_devices()
    for did, device in devices.items():
        print(device)
        devices_list.append(device)


get_cloud_device()


@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    for device in devices_list:
        if device.name not in exclude:
            DeviceData.create_metrics_data(device, registry)

    text = generate_latest(registry)
    return Response(text, status=200, mimetype='text/plain')


if __name__ == '__main__':
    app.run()
