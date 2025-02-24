from yaml import safe_load
from miio import Device
from miio.cloud import CloudInterface


def verify_device_config(device_yaml, did, token, ip):
    # 获取设备信息
    services = device_yaml.get("devices")[0]["services"]

    # 初始化设备对象
    dev = Device(ip, token)

    # 遍历所有services和properties
    for service in services:
        siid = service.get("siid")
        properties = service.get("properties", [])

        for prop in properties:
            # 检查是否支持读取
            if "read" in prop.get("access"):
                piid = prop.get("piid")
                name = prop.get("name")
                standard_name = prop.get("standard_name")
                description_cn = prop.get("description_cn")
                description = prop.get("description")
                prop_format = prop.get("format")
                unit = prop.get("unit")
                value_range = prop.get("value-range", [])

                result = dev.send("get_properties", [{'did': did, 'siid': siid, 'piid': piid}])
                value = result[0].get('value')

                text = f"standard_name: {standard_name}, name: {name}, description_cn: {description_cn}, description: {description}, value: {value}, format: {prop_format}, unit: {unit}"
                if value_range:
                    text += f", 范围：{value_range[0]}~{value_range[1]}, 步长：{value_range[2]}"
                print(text)


if __name__ == '__main__':
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = safe_load(file)
        cloud = CloudInterface(config.get("username"), config.get("password"))
        devices = cloud.get_devices()
        with open('device.yaml', 'r', encoding='utf-8') as yaml_file:
            device_yaml = safe_load(yaml_file)
            model = device_yaml.get('devices')[0].get('model')
            for device in devices.values():
                if device.model == model and device.name == '软路由':
                    print(device)
                    verify_device_config(device_yaml, device.did, device.token, device.ip)
                    break
