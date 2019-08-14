# !/usr/bin/env python
# -*- coding:utf-8 -*-


class Format(object):

    def __init__(self, poi_strs):
        self.poi_strs = poi_strs

    def split(self):
        points = []
        for poi_str in self.poi_strs:
            lng = float(poi_str.split(',')[1])
            lat = float(poi_str.split(',')[2])
            point = {'lng': lng, 'lat': lat}
            points.append(point)
        return points


if __name__ == '__main__':
    pois = ['四川省交通运输厅公路局医院,103.966889,30.760965,医疗保健服务;综合医院;综合医院', '四川省人民医院金牛医院(装修中),104.029597,30.706523,医疗保健服务;综合医院;综合医院', '交大东门宾馆(九里欣居北),104.057388,30.699082,住宿服务;宾馆酒店;宾馆酒店', '四川省林业中心医院,104.066785,30.683221,医疗保健服务;综合医院;综合医院']
    form = Format(pois)
    print(form.split())