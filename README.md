# miio-exporter
基于小米设备的Prometheus exporter

支持prometheu和prometheu-pushgateway

prometheu-pushgateway 支持 HTTP Basic Auth 认证

目前支持的设备：

* 米家智能插座2 蓝牙网关版
* 米家智能插座3


## 使用方式
1. 将config-sample.yaml重命名为config.yaml
2. 填入自己的米家账号，用include写入需要监控的设备名
3. 安装依赖并启动
    ```shell
    pip install -r requirements.txt
    python app.py
    ```
4.浏览器访问http://127.0.0.1/metrics