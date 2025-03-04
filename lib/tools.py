# -*- coding: utf-8 -*-
# File: tools.py
# Time: 2025/3/2 17:41
# Author: jiaxin
# Email: 1094630886@qq.com

from miio.device import Device
from miio.cloud import CloudInterface
from prometheus_client import CollectorRegistry, Gauge
from yaml import safe_load
from lib.logger import logger


def load_config_and_devices(config_path="config.yaml"):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as file:
        config = safe_load(file)
    logger.setLevel(config.get("log_level", "INFO").upper())
    logger.info("配置加载完成。。。")

    # 获取设备列表
    config['devices_list'] = get_cloud_devices(
        config["username"], config["password"],
        include=config.get("include", []),
        exclude=config.get("exclude", [])
    )

    logger.info("设备列表加载完成")
    return config


def create_metrics_registry(config):
    """根据配置文件初始化 Prometheus 指标"""
    registry = CollectorRegistry()
    metrics_list = {}
    for device in config.get('devices', {}).values():
        for service in device.get('services', []):
            for property in service.get('properties', []):
                standard_name = property.get('standard_name')
                if standard_name not in metrics_list:
                    doc = property.get('description_cn', "")
                    if property.get('unit'):
                        doc += f" 单位：{property.get('unit')}"
                    if property.get('value-range'):
                        doc += f" 取值范围：{property.get('value-range')[0]} ~ {property.get('value-range')[1]} 步长：{property.get('value-range')[2]}"
                    metrics_list[standard_name] = Gauge(
                        standard_name, doc,
                        labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                        registry=registry
                    )
    return registry, metrics_list


def get_cloud_devices(username, password, include=None, exclude=None):
    """从小米云平台获取设备列表"""
    logger.info("云平台查询设备中，请等待。。。")
    cloud = CloudInterface(username, password)
    devices = cloud.get_devices()
    devices_list = []
    for did, device in devices.items():
        logger.info(device)
        if include:
            if device.name in include:
                devices_list.append(device)
        elif exclude:
            if device.name not in exclude:
                devices_list.append(device)
        else:
            devices_list.append(device)
    logger.info(f"监控的设备：{devices_list}")
    return devices_list


def fetch_device_properties(ip, token, device_config):
    """获取设备属性数据"""
    device = Device(ip=ip, token=token)
    data = {}
    for service in device_config.get('services', []):
        for property in service.get('properties', []):
            standard_name = property.get('standard_name')
            parameters = [{
                'did': str(device.device_id),
                'siid': service.get('siid'),
                'piid': property.get('piid')
            }]
            try:
                response = device.send('get_properties', parameters)
                data[standard_name] = response[0].get('value')
            except Exception as e:
                logger.error(f"获取设备数据失败：{e}")
    logger.info(data)
    return data


def update_metrics_from_device_data(config, metrics_list):
    """更新 Prometheus 指标数据"""
    for device in config.get('devices_list'):
        device_config = config['devices'][device.model]
        data = fetch_device_properties(device.ip, device.token, device_config)
        for service in device_config.get('services', []):
            for property in service.get('properties', []):
                standard_name = property.get('standard_name')
                if standard_name != "cycle_data_value":
                    value = data.get(standard_name)
                    if value is not None:
                        metric = metrics_list.get(standard_name)
                        if metric:
                            metric.labels(
                                did=device.did, name=device.name, model=device.model,
                                ip=device.ip, ssid=device.ssid, mac=device.mac
                            ).set(value)
