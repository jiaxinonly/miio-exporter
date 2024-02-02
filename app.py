from flask import Flask, Response
from miio.cloud import CloudInterface
from miio.chuangmi_plug import ChuangmiPlug
from miio.device import Device
import re
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from lib.tools import DeviceData

username = ""
password = ""
exclude = ['热水器', '米家纯净式智能加湿器 2 lite', '米家直流变频两季扇', '空调插座', '温湿度传感器2', '温湿度传感器']
devices_list = []
app = Flask(__name__)

registry = CollectorRegistry()
plug_online = Gauge('plug_online', '智能插座在线状态', labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                    registry=registry)
plug_switch = Gauge(name='plug_switch', documentation="智能插座开关状态",
                    labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
plug_led = Gauge(name="plug_led", documentation="智能插座LED灯状态",
                 labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)

plug_power = Gauge("plug_power", "智能插座功率",
                   labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
plug_temperature = Gauge("plug_temperature", "智能插座温度", labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                         registry=registry)
plug_usb_switch = Gauge("plug_usb_switch", "智能插座", labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                        registry=registry)


def get_cloud_device():
    cloud = CloudInterface(username, password)
    devices = cloud.get_devices()
    for did, device in devices.items():
        print(device)
        devices_list.append(device)


get_cloud_device()


@app.route('/metrics')
def metrics():
    for device in devices_list:
        if device.name not in exclude:
            DeviceData.get_device_data(device)

    text = generate_latest(registry)
    return Response(text, status=200, mimetype='text/plain')


if __name__ == '__main__':
    app.run()
