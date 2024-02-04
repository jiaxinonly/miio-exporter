from miio.chuangmi_plug import ChuangmiPlug
from miio.device import Device
from prometheus_client import CollectorRegistry, Gauge, generate_latest


class DeviceData:
    @staticmethod
    def get_device_data(device):
        if device.model == 'chuangmi.plug.v3':
            chuangmi = ChuangmiPlug(ip=device.ip, token=device.token)
            status = chuangmi.status()
            data = {
                'plug_online': status.is_on,
                'plug_led': status.led,
                'plug_power': status.load_power,
                'plug_switch': status.power,
                'plug_temperature': status.temperature,
                'plug_usb_switch': status.usb_power
            }
            return data
        elif device.model == 'chuangmi.plug.212a01':
            dev = Device(ip=device.ip, token=device.token)
            switch = dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 1}])[0]['value']
            temperature = dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 6}])[0]['value']
            work_time = dev.send("get_properties", [{'did': device.did, 'siid': 2, 'piid': 7}])[0]['value']
            led = dev.send("get_properties", [{'did': device.did, 'siid': 3, 'piid': 1}])[0]['value']
            Power_Consumption = dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 1}])[0]['value']
            Electric_Current = dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 2}])[0]['value']
            Voltage = dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 3}])[0]['value']
            Electric_Power = dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 6}])[0]['value']
            Surge_power = dev.send("get_properties", [{'did': device.did, 'siid': 5, 'piid': 7}])[0]['value']

            date = {
                'plug_switch': switch,
                'plug_temperature': temperature,
                'plug_work_time': work_time,
                'plug_led': led,
                'plug_Power_Consumption': Power_Consumption,
                'plug_Electric_Current': Electric_Current,
                'plug_Voltage': Voltage,
                'plug_Electric_Power': Electric_Power,
                'plug_Surge_power': Surge_power
            }
            return date

    @staticmethod
    def create_metrics_data(device, registry):
        if device.model == 'chuangmi.plug.v3':
            plug_online = Gauge('plug_online', '智能插座在线状态',
                                labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                registry=registry)
            plug_switch = Gauge(name='plug_switch', documentation="智能插座开关状态",
                                labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
            plug_led = Gauge(name="plug_led", documentation="智能插座LED灯状态",
                             labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)

            plug_power = Gauge("plug_power", "智能插座功率",
                               labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
            plug_temperature = Gauge("plug_temperature", "智能插座温度",
                                     labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                     registry=registry)
            plug_usb_switch = Gauge("plug_usb_switch", "智能插座",
                                    labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                    registry=registry)
            data = DeviceData.get_device_data(device)
            plug_online.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                               mac=device.mac).set(data['plug_online'])
            plug_switch.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                               mac=device.mac).set(data['plug_switch'])
            plug_led.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                            mac=device.mac).set(data['plug_led'])
            plug_power.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                              mac=device.mac).set(data['plug_power'])
            plug_temperature.labels(did=device.did, name=device.name, model=device.model, ip=device.ip,
                                    ssid=device.ssid, mac=device.mac).set(data['plug_temperature'])
            plug_usb_switch.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_usb_switch'])
            return True
        elif device.model == 'chuangmi.plug.212a01':
            # plug_online = Gauge('plug_online', '智能插座在线状态',
            #                     labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
            #                     registry=registry)
            plug_switch = Gauge(name='plug_switch', documentation="智能插座开关状态",
                                labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
            plug_led = Gauge(name="plug_led", documentation="智能插座LED灯状态",
                             labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)

            # plug_power = Gauge("plug_power", "智能插座功率",
            #                    labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'], registry=registry)
            plug_temperature = Gauge("plug_temperature", "智能插座温度",
                                     labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                     registry=registry)

            plug_Power_Consumption = Gauge("plug_Power_Consumption", "总耗电量",
                                    labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                    registry=registry)
            plug_Electric_Current = Gauge("plug_Electric_Current", "电流",
                                          labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                          registry=registry)
            plug_Voltage = Gauge("plug_Voltage", "电压",
                                          labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                          registry=registry)
            plug_Electric_Power = Gauge("plug_Electric_Power", "功率",
                                          labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                          registry=registry)
            plug_Surge_power = Gauge("plug_Surge_power", "电涌",
                                          labelnames=['did', 'name', 'model', 'ip', 'ssid', 'mac'],
                                          registry=registry)
            data = DeviceData.get_device_data(device)
            # plug_online.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
            #                    mac=device.mac).set(data['plug_online'])
            plug_switch.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                               mac=device.mac).set(data['plug_switch'])
            plug_led.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                            mac=device.mac).set(data['plug_led'])
            # plug_power.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
            #                   mac=device.mac).set(data['plug_power'])
            plug_temperature.labels(did=device.did, name=device.name, model=device.model, ip=device.ip,
                                    ssid=device.ssid, mac=device.mac).set(data['plug_temperature'])

            plug_Power_Consumption.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_Power_Consumption'])
            plug_Electric_Current.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_Electric_Current'])
            plug_Voltage.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_Voltage'])
            plug_Electric_Power.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_Electric_Power'])
            plug_Surge_power.labels(did=device.did, name=device.name, model=device.model, ip=device.ip, ssid=device.ssid,
                                   mac=device.mac).set(data['plug_Surge_power'])

            return True
