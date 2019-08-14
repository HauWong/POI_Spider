# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import xlsxwriter
import urllib
from urllib import request
from Transform import transform


def get_location(provinces, key):
    locations_list = {}
    for p in provinces:
        print(p)
        url = generate_url(p, key)
        json_obj = request.urlopen(url)
        data = json.load(json_obj)
        print(data)
        if '市' in p:
            districts = data['districts'][0]['districts'][0]['districts']
        else:
            districts = data['districts'][0]['districts']
        for dist in districts:
            city_name = dist['name']
            city_center = transform.Transform(dist['center']).gcj_to_wgs().split('\t')
            # city_center = dist['center']
            # text = p+city_name + ': ' + city_center
            locations_list[p+city_name] = [float(city_center[0]), float(city_center[1])]
    return locations_list


def generate_url(province, key):
    if '市' in province:
        subdistrict = 2
    else:
        subdistrict = 1
    p = urllib.parse.quote(province)
    url = 'http://restapi.amap.com/v3/config/district?keywords=' + p + \
        '&subdistrict=' + str(subdistrict) + '&output=json&key=' + key
    return url


def save_to_file(path, loc_dict):
    # work_xlsx = xlsxwriter.Workbook(path)
    # work_sheet = work_xlsx.add_worksheet()
    # for row in range(0, len(loc_list)):
    #     info = loc_list[row].split('\t')
    #     for col in range(0, len(info)):
    #         value = info[col]
    #         if (col == 1 or col == 2) and row != 0:
    #             value = float(value)
    #         work_sheet.write(row, col, value)
    # work_xlsx.close()

    with open(path, 'w') as f:
        f.write(str(loc_dict))


if __name__ == '__main__':
    provinces = ['北京市', '上海市', '天津市', '广东省', '浙江省', '江苏省', '福建省', '湖南省', '湖北省', '重庆市',
                 '辽宁省', '吉林省', '黑龙江省', '河北省', '河南省', '山东省', '陕西省', '甘肃省', '青海省',
                 '新疆维吾尔自治区','山西省', '四川省', '贵州省', '安徽省', '江西省', '云南省', '内蒙古自治区',
                 '广西壮族自治区', '西藏自治区','宁夏回族自治区', '海南省']

    key = 'a725234836f057fc777e441dffc06bc7'

    path = r'd:/desktop/district_locations.txt'

    district_location = get_location(provinces, key)
    print('共', len(district_location), '个城市或区')
    save_to_file(path, district_location)