# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import random

import json

import Retrieval.trim as trim
import Retrieval.poi as poi
import Retrieval.ip_agent as ip_agent

ip_pool = 'https://www.kuaidaili.com/free/inha'
# TODO: 修改i高德地图开发者Key
api_key_list = ['a725234836f057fc777e441dffc06bc7', 'd77bd65d7a8b0ede40e8060b7ec410d7',
                '4c38edf1344aa853060b7f930be5e7c3', 'be0370dd7d6056803bc8c64d901cfd0d',
                '331fd8655d481098466ddeb5f0161276']
# 上述Key已失效，用户可前往高德开放平台(https://lbs.amap.com/)自行申请。 ----2020.12.14 16:28

# 原始POI类型
motor = ['加油站|加气站|其他能源站', '汽车养护|洗车场|汽车俱乐部|汽车救援|汽车配件销售|汽车租赁|二手车交易',
         '汽车销售', '汽车维修']
repast = ['中餐厅|外国餐厅|快餐厅', '咖啡厅|茶艺馆|冷饮店', '糕饼店|甜品店', '休闲餐饮场所']
shopping = ['商场|便民商店|超级市场', '家电电子卖场|花鸟鱼虫市场|家居建材市场|综合市场|服装鞋帽皮具店',
            '文化用品店|体育用品店', '个人用品店', '专卖店', '特殊买卖场所']
life = ['旅行社', '物流速递', '电讯营业厅', '人才市场', '美容美发店|洗浴推拿场所', '事务所']
sport = ['运动场馆', '娱乐场所', '休闲场所', '影剧院', '度假疗养所']
medical = ['综合医院', '专科医院|动物医疗场所', '诊所', '急救中心|疾病预防机构', '医药保健销售店']
hotel = ['四星级宾馆|五星级宾馆|奢华宾馆', '三星级宾馆', '经济型连锁酒店', '旅馆招待所', '青年旅舍']
scene = ['公园广场', '风景名胜']
house = ['产业园区', '商务写字楼|工业大厦建筑物', '商住两用楼宇', '别墅', '住宅小区', '宿舍', '社区中心']
government = ['政府机关|外国机构', '民主党派|社会团体', '公检法机构|交通车辆管理|工商税务机构']
culture = ['博物馆|展览馆|会展中心|美术馆|图书馆|科技馆|文化宫|天文馆|档案馆', '文艺团体|传媒机构', '高等院校|中学|小学',
           '幼儿园', '成人教育|职业技术学校', '学校内部设施', '科研机构', '培训机构']
transport = ['机场相关|火车站|港口码头', '停车场']
financial = ['银行|保险公司|证券公司|财务公司']
company = ['知名企业|广告装饰|建筑公司|医药公司|机械电子|冶金化工|网络科技|商业服务|电信公司|矿产公司', '工厂',
           '农林牧渔基地']

# 聚合后的POI类型
residential = ['社区中心|别墅|住宅小区|宿舍']
market_recreation = ['汽车销售|汽车租赁|汽车配件销售|二手车交易|物流速递|购物服务']
service_buindling = ['商务写字楼|银行|保险公司|证券公司|财务公司']
amusement = ['住宿服务|餐饮服务|美容美发店|洗浴推拿场所|娱乐场所|休闲场所|电影院']
industrial = ['工厂']
hospital = ['综合医院']
educational = ['高等院校|中学|小学|科研机构']
administrative = ['政府机关|外国机构|民主党派|社会团体|公检法机构|交通车辆管理|工商税务机构']
public = ['博物馆|展览馆|会展中心|美术馆|图书馆|科技馆|文化宫|音乐厅|剧场|天文馆|档案馆|综合场馆|加油站|加气站|火车站|港口码头']


# TODO: 修改POI类型
all_types = {'residential': residential, 'market': market_recreation, 'service': service_buindling, 'public': public,
             'amusement': amusement, 'industrial': industrial, 'medical': hospital, 'educational': educational,
             'administrative': administrative}


def flatten_locs(regions_dict):

    """将块坐标字典转换为列表"""

    res_ls = []
    for region_name in regions_dict.keys():
        plg_list = regions_dict[region_name]
        for plg in plg_list:
            res_ls.append(plg)
    return res_ls


def generate_locs(rect_loc, num_grid):

    """将目标区域分成几块，得到所有块的范围坐标字符串列表"""

    res = []
    nw_lon, nw_lat, se_lon, se_lat = rect_loc
    lon_gap = (se_lon - nw_lon)/num_grid[0]
    lat_gap = (nw_lat - se_lat)/num_grid[1]
    cur_nw_lon = nw_lon
    cur_nw_lat = nw_lat
    for r in range(num_grid[1]):
        for c in range(num_grid[0]):
            res.append('%.6f,%.6f|%.6f,%.6f|%.6f,%.6f|%.6f,%.6f|%.6f,%.6f' % \
                       (cur_nw_lon+c*lon_gap, cur_nw_lat-r*lat_gap,
                        cur_nw_lon+(c+1)*lon_gap, cur_nw_lat-r*lat_gap,
                        cur_nw_lon+(c+1)*lon_gap, cur_nw_lat-(r+1)*lat_gap,
                        cur_nw_lon+c*lon_gap, cur_nw_lat-(r+1)*lat_gap,
                        cur_nw_lon+c*lon_gap, cur_nw_lat-r*lat_gap))
    return res


def start_retrieval(plg_loc_str, par_path, ip_page_index):

    """获取一块区域的POI"""
    # ip_page_index = ip_page_index % 400
    ip_url = '%s/%d' % (ip_pool, ip_page_index)
    ip_type_list, ip_port_list = ip_agent.get_ip(ip_url, ('HTTP', '168.195.192.107:8080'))
    ip = [ip_type_list, ip_port_list]
    print(plg_loc_str)
    for word_type in all_types:
        poi_type_ls = all_types[word_type]
        file_path = os.path.join(par_path, '%s.xlsx' % word_type)
        for type_idx in range(0, len(poi_type_ls)):
            poi_type = poi_type_ls[type_idx]
            print(poi_type)
            key_idx = random.randint(0, len(api_key_list)-1)
            api_key = api_key_list[key_idx]
            p = poi.Poi(poi_type, plg_loc_str, api_key, ip)
            p.gaode_search()
            p.save_append(file_path, type_idx)

# ---------------------------------------Start-------------------------------------------
print('保存POI类型 ...')
save_list = []
# TODO: 修改POI类型保存路径
poi_type_save_path = r'D:\Documents\Study\Python\Self_Supervision\data\poi_types.txt'
with open(poi_type_save_path, 'w') as f:
    for w_type in all_types:
        poi_type_list = all_types[w_type]
        for i in range(0, len(poi_type_list)):
            cur_type_str = '%s_%02d' % (w_type, i)
            save_list.append(cur_type_str)
    js = json.dumps(save_list)
    f.write(js)

# TODO: 修改坐标范围文件路径
locations_path = r'..\assistants\test_samples.json'
with open(locations_path, 'r') as loc_f:
    js = loc_f.read()
    r_dict = json.loads(js)
    print(r_dict)
locations_ls = flatten_locs(r_dict)

# r_dict = {'1': generate_locs([116.199, 40.024, 116.555, 39.753], (4, 4))}
# locations_ls = r_dict['1']

print('开始获取数据 ... ')
ip_idx = 1
region_name_list = list(r_dict.keys())
for k in range(0, len(region_name_list)):
    region_name = region_name_list[k]

    # 针对多边形文件
    num = len(locations_ls)
    for i in range(1, num+1):
        print(i)
        locs_str = locations_ls[i-1]
        # TODO: 修改POI保存路径，保证为空文件夹
        path = os.path.join(r'D:\Documents\Study\Python\Data_Model\data\beijing\POI\hotel', region_name, '%04d' % i)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        start_retrieval(locs_str, path, i)
        trim.merge_multi_poi(path)

    # 针对自动生成的规则窗口
    # print(k)
    # path = os.path.join(r'D:\Documents\Study\Python\Self_Supervision\data\shijiazhuang\regular_pois', region_name)
    # folder = os.path.exists(path)
    # if not folder:
    #     os.makedirs(path)
    # loc_str = r_dict[region_name]
    # start_retrieval(loc_str, path, ip_idx)
    # trim.merge_multi_poi(path)
    # ip_idx += 1

print('数据获取完毕.')
