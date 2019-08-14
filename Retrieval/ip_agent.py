# !/usr/bin/env python
# -*- coding:utf-8 -*-

import random

from urllib import request
import re


def get_ip(url, start_ip):
    proxy = {start_ip[0]: start_ip[1]}
    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0 Safari/537.36 OPR/15.0',
                       'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko']
    user_agent_idx = random.randint(0, len(user_agent_list) - 1)
    opener.addheaders = [('User-Agent', user_agent_list[user_agent_idx])]
    request.install_opener(opener)

    res = request.urlopen(url)
    html = res.read()
    html = html.decode('utf-8')

    # xiladaili
    # ip_pattern = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+):\d+</td>')
    # port_pattern = re.compile(r'<td>\d+\.\d+\.\d+\.\d+:(\d+)</td>')
    # types_pattern = re.compile(r'<td>([A-Za-z]+\,?[A-Za-z]+?[\u4e00-\u9fa5]+)</td>')

    # kuaidaili
    ip_pattern = re.compile(r'<td data-title="IP">(\d+\.\d+\.\d+\.\d+)</td>')
    port_pattern = re.compile(r'<td data-title="PORT">(\d+)</td>')
    types_pattern = re.compile(r'<td data-title="类型">([A-Za-z]+)</td>')

    ip_list = re.findall(ip_pattern, html)
    port_list = re.findall(port_pattern, html)
    types_list = re.findall(types_pattern, html)

    ip_port_list = []
    type_list = []
    for i in range(len(ip_list)):
        type_list.append(types_list[i].split(',')[0])
        ip_port = ip_list[i] + ':' + port_list[i]
        ip_port_list.append(ip_port)

    return type_list, ip_port_list
