from miio.chuangmi_plug import ChuangmiPlug
from miio.device import Device
class DeviceData:
    @staticmethod
    def get_device_data(device):
        if device.model == 'chuangmi.plug.v3':
            chuangmi = ChuangmiPlug(ip=device.ip, token=device.token)
            status = chuangmi.status()
            data = {
                'did': device.did,
                'name': device.name,
                'model': device.model,
                'ip': device.ip,
                'ssid': device.ssid,
                'mac': device.mac,
                'online': status.is_on,
                'led': status.led,
                'power': status.load_power,
                'switch': status.power,
                'temperature': status.temperature,
                'usb_switch': status.usb_power
            }
            return data
        elif device.model == 'chuangmi.plug.212a01':
            dev = Device(ip=device.ip, token=device.token)
            print(dev)
            print(dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 1}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 6}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 7}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 3, 'piid': 1}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 1}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 2}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 3}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 6}]))
            print(dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 7}]))
