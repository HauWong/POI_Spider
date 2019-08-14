# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import math
from urllib import request, error

pi = 3.1415926535897932384626
ee = 0.00669342162296594323
a = 6378245.0


class Transform(object):

    """
    参数输入的两种方式要求统一格式
    数字格式：par1 = lng, par2 = lat；
    字符串格式：par1 = 'lng, lat'
    """
    def __init__(self, par1, par2=-1):
        if par2 == -1:
            self.lng = float(par1.split(',')[0])
            self.lat = float(par1.split(',')[1])
            self.gaode_loc_str = str(self.lng) + ',' + str(self.lat)
        else:
            self.lng = par1
            self.lat = par2
            self.gaode_loc_str = str(self.lng) + ',' + str(self.lat)

    def wgs_to_gcj(self, gaode_key, opener):

        # 注：该函数返回结果为高德格式的坐标字符串，即'lng, lat'
        request.install_opener(opener)
        try:
            req = request.urlopen('https://restapi.amap.com/v3/assistant/coordinate/convert?locations=%s'
                                 '&coordsys=gps&output=json&key=%s' % (self.gaode_loc_str, gaode_key))
        except error.URLError:
            return False
        ret = json.load(req)
        req.close()
        loc = ret['locations']
        return loc

    def gcj_to_wgs(self):
        loc = self.transform(self.lat, self.lng)
        lat_res = str(self.lat*2 - loc[0])
        lng_res = str(self.lng*2 - loc[1])
        loc_str = lng_res + '\t' + lat_res
        return loc_str

    def transform(self, lat, lng):
        dlat = self.trans_lat(lng - 105.0, lat - 35.0)
        dlng = self.trans_lng(lng - 105.0, lat - 35.0)

        radLat = lat / 180.0 * pi
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * pi)
        dlng = (dlng * 180.0) / (a / sqrt_magic * math.cos(radLat) * pi)
        mg_lat = lat + dlat
        mg_lng = lng + dlng

        return [mg_lat, mg_lng]

    def trans_lat(self, x, y):
        res = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
        res += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        res += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
        res += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
        return res

    def trans_lng(self, x, y):
        res = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
        res += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
        res += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
        res += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0;
        return res


def dms_to_ten(dms_str):
    degree, minute, second = dms_str.split(' ')
    return int(degree)+int(minute)/60+float(second)/3600


def ten_to_dms(ten_value):
    degree = math.floor(ten_value)
    tmp = (ten_value-degree)*60
    minute = math.floor(tmp)
    second = (tmp-minute)*60

    return '%d %d %f' % (degree, minute, second)


if __name__ == '__main__':
    loc_l = ['104 0 7.44', '30 43 40.35', '104 5 34.55', '30 40 4.88']
    for loc in loc_l:
        print(dms_to_ten(loc))