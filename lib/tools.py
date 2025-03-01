from miio.device import Device
from prometheus_client import CollectorRegistry, Gauge
from miio.cloud import CloudInterface
from yaml import safe_load


class Config:
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = safe_load(file)
        print(config)
        username = config.get("username", "")
        password = config.get("password", "")
        include = config.get("include", [])
        exclude = config.get("exclude", [])
        devices = config.get('devices', [])
        registry = CollectorRegistry()
        metrics = {}
        for device in devices.values():
            print(device)
            for service in device.get('services'):
                for propertie in service.get('properties'):
                    doc = propertie.get('description_cn')
                    if propertie.get('unit'):
                        doc += f" 单位：{propertie.get('unit')}"
                    if propertie.get('value-range'):
                        doc += f" 取值范围：{propertie.get('value-range')[0]} ~ {propertie.get('value-range')[1]} 步长：{propertie.get('value-range')[2]}"
                    metrics[propertie.get('standard_name')] = Gauge(propertie.get('standard_name'), doc,
                                                                    labelnames=['did', 'name', 'model', 'ip', 'ssid',
                                                                                'mac'], registry=registry)


def get_cloud_device():
    cloud = CloudInterface(Config.username, Config.password)
    devices = cloud.get_devices()
    devices_list = []
    for did, device in devices.items():
        print(device)
        # 如果配置了 include，则只处理 include 中的设备
        if Config.include:
            if device.name in Config.include:
                devices_list.append(device)
        elif Config.exclude:
            if device.name not in Config.exclude:
                # 如果没有配置 include，则处理除 exclude 外的设备
                devices_list.append(device)
        else:
            devices_list.append(device)
    return devices_list


class DeviceData:
    @staticmethod
    def get_device_data(ip, token):
        device = Device(ip=ip, token=token)
        services = Config.devices[device.model]['services']
        data = {}
        for service in services:
            for propertie in service.get('properties'):
                if "read" in propertie.get("access"):
                    standard_name = propertie.get('standard_name')
                    parameters = [{
                        'did': str(device.device_id),
                        'siid': service.get('siid'),
                        'piid': propertie.get('piid')
                    }]
                    data[standard_name] = device.send('get_properties', parameters)[0].get('value')
        print(data)
        return data

    @staticmethod
    def create_metrics_data(device):
        data = DeviceData.get_device_data(device.ip, device.token)
        for service in Config.devices.get(device.model).get('services'):
            for propertie in service.get('properties'):
                standard_name = propertie.get('standard_name')
                value = data.get(standard_name)
                print(standard_name, value)
                Config.metrics.get(standard_name).labels(did=device.did, name=device.name, model=device.model,
                                                         ip=device.ip, ssid=device.ssid,
                                                         mac=device.mac).set(data.get(standard_name))
        return True