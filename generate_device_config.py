import json
import yaml
import requests


def get_device_spec(device_type: str):
    url = f"https://home.miot-spec.com/spec?type={device_type}"
    headers = {
        "content-type": "application/json",
        "x-inertia": "true",
        "x-inertia-version": "c222c6ebdcb6f8bc1d1b321b7a051592",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.text)
        device_spec = response.json()
        return device_spec
    else:
        print(f'请求失败，状态码：{response.status_code}')


def convert_device_spec_to_yaml(device_spec: dict):
    # 提取需要的字段
    product = device_spec.get("props", {}).get("product", {})
    spec = device_spec.get("props", {}).get("spec", {})

    model = product.get("model", "")
    # 初始化YAML数据结构
    yaml_data = {
        "devices": {
            model : {
                "model": model,
                "name": product.get("name", ""),
                "services": []
            }
        }
    }
    services = dict(sorted(spec.get("services", {}).items(), key=lambda item: int(item[0])))

    # 遍历services并提取信息
    for service in services.values():
        service_info = {
            "name": service.get("name", ""),
            "description": service.get("description", ""),
            "siid": service.get("iid", 0),
            "properties": []
        }

        # 遍历properties并提取信息
        for prop in service.get("properties", {}).values():
            if "read" in prop.get('access'):
                prop_info = {
                    "name": prop.get("name", ""),
                    "standard_name": prop.get("name", "").replace("-", "_"),  # 默认跟name一致，然后手动替换
                    "description": prop.get("description", ""),
                    "description_cn": "",  # 空值，手动输入
                    "piid": prop.get("iid", 0),
                    "format": prop.get("format", ""),
                    "unit": prop.get("unit", ""),
                    "access": prop.get("access", []),
                    "value-range": prop.get("value-range", [])
                }
                service_info["properties"].append(prop_info)

        yaml_data["devices"][model]["services"].append(service_info)

    # 将YAML数据写入文件
    with open("device.yaml", 'w', encoding='utf-8') as yaml_file:
        yaml.dump(yaml_data, yaml_file, allow_unicode=True, sort_keys=False)

    print(f"device.yaml文件已生成")


if __name__ == '__main__':
    device_spec = get_device_spec("urn:miot-spec-v2:device:outlet:0000A002:cuco-v3:2")
    convert_device_spec_to_yaml(device_spec)
