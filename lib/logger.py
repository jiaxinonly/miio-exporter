# -*- coding: utf-8 -*-
# File: logger.py
# Time: 2025/3/1 20:11
# Author: jiaxin
# Email: 1094630886@qq.com
import logging

formatter = logging.Formatter('[%(asctime)s] %(filename)s line %(lineno)d - %(levelname)s: %(message)s')
logger = logging.getLogger("miio-exporter")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
