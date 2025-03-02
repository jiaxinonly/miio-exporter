# -*- coding: utf-8 -*-
# File: logger.py
# Time: 2025/3/1 20:11
# Author: jiaxin
# Email: 1094630886@qq.com

import logging

# 创建 logger
logger = logging.getLogger("miio-exporter")
logger.setLevel(logging.INFO)  # 默认日志级别为 INFO

# 定义日志格式
formatter = logging.Formatter('[%(asctime)s] %(filename)s line %(lineno)d - %(levelname)s: %(message)s')

# 创建控制台处理器
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# 添加处理器到 logger
logger.addHandler(stream_handler)