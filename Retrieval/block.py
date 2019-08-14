# !/usr/bin/env python
# -*- coding:utf-8 -*-


class BaiduDiv(object):

    """
    坐标输入格式：
    loc_all = 'lat_sw,lng_sw,lat_ne,lng_ne'

    最终返回格式：
    'lat_sw,lng_sw,lat_ne,lng_ne'
    """
    def __init__(self, loc_all, bias):
        self.loc_all = loc_all
        self.bias = bias

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne-lat_sw+0.0001)/self.bias)):
            lat_list.append(lat_sw+self.biasi)
        lat_list.append(lat_ne)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne-lng_sw+0.0001)/self.bias)):
            lng_list.append(lng_sw+self.bias*i)
        lng_list.append(lng_ne)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for j in range(0, len(l2)):
                b = str(l2[j])
                ab = a+','+b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for i in range(0, len(l1)-1):
            for j in range(0, len(l2)-1):
                a = ls_com_v[len(l2)*i+j]
                b = ls_com_v[len(l2)*(i+1)+j+1]
                ab = a+','+b
                ls.append(ab)
        return ls


class GaodeDiv(object):

    """
    坐标输入格式：
    loc_all = 'lng_nw,lat_nw,lng_se,lat_se'
    最终返回格式：
    'lng_nw,lat_nw,lng_se,lat_se'
    """
    def __init__(self, loc_all, bias):
        self.loc_all = loc_all
        self.bias = bias

    # 以一定间隔对经度进行划分，返回一个列表
    def lng_all(self):
        lng_nw = float(self.loc_all.split(',')[0])
        lng_se = float(self.loc_all.split(',')[2])
        lng_list = [lng_nw]
        for i in range(1, int((lng_se - lng_nw + 0.0001)/self.bias)):
            lng_list.append(lng_nw + self.bias*i)
        lng_list.append(lng_se)
        return lng_list

    # 以一定间隔对纬度进行划分，返回一个列表
    def lat_all(self):
        lat_nw = float(self.loc_all.split(',')[1])
        lat_se = float(self.loc_all.split(',')[3])
        lat_list = [lat_se]
        for i in range(1, int((lat_nw - lat_se + 0.0001)/self.bias)):
            lat_list.append(lat_se + self.bias*i)
        lat_list.append(lat_nw)
        lat_list.reverse()
        return lat_list

    # 将经纬度组合
    def ls_com(self):
        l1 = self.lng_all()
        l2 = self.lat_all()
        ab_list = []
        for i in range(0, len(l2)):
            lat = '%.6f'%(l2[i])
            for j in range(0, len(l1)):
                lng = '%.6f'%(l1[j])
                ab = lng+','+lat
                ab_list.append(ab)
        return ab_list

    # 将对角线坐标进行组合
    def ls_row(self):
        l1 = self.lng_all()
        l2 = self.lat_all()
        ls_com_v = self.ls_com()
        ls = []
        for i in range(0, len(l2)-1):
            for j in range(0, len(l1)-1):
                a = ls_com_v[len(l1)*i+j]
                b = ls_com_v[len(l1)*(i+1)+j+1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


if __name__ == '__main__':
    loc = GaodeDiv('114.498887,38.050120,114.501838,38.048102', 0.025)
    for i in loc.ls_row():
        print(i)