import requests
import json
import os
import random
import time
import sys

max_year = time.localtime(time.time())[0]
path = os.path.abspath(os.path.dirname(__file__))
u_a = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42']
gaokao_type_arr = ['1', '2', '3', '2073','2074']
score_type_arr = ['1', '2', '3']
start_time = time.time()

def research():

    # 解析文件province.json
    file = open(path+'\\province.json', mode='r', encoding='utf-8')
    dict_obj = dict(json.load(file))
    file.close()
    province_part = dict_obj['data']['province']

    # 遍历
    # for letter in [chr(i) for i in range(ord('A'), ord('A')+26)]: # 遍历26个字母
    #     if letter in province_part : # 有没有所在的字母
    #         for dic in province_part[letter]: # pro这里是一个列表,这里开始遍历每一个省份
    #             province_id, province_name = str(dic['province_id']),dic['province_name']
    #             for year in [str(t) for t in range(2014,max_year+1)]:
    #                 for gaokao_type in gaokao_type_arr:
    #                     for score_type in score_type_arr:
    #                         get_infor(province = province_name,\
    #                                 year = year,\
    #                                 province_id = province_id,\
    #                                 gaokao_type = gaokao_type,\
    #                                 score_type = score_type)
    #                         time.sleep( random.randint(1000,2000)/1000 ) # 随机暂停1到2秒

    # 重写
    for province_id,province_name in province_part.items() : 
        for year in [str(t) for t in range(2014,max_year+1)]:
            for gaokao_type in gaokao_type_arr:
                for score_type in score_type_arr:
                    t = time.time()
                    now_time = time.ctime(t)
                    cost_time = t - start_time
                    print(f'当前时间:{now_time},当前花费时间:{cost_time}秒,爬取{province_id},{province_name}的{year}的一分一段')
                    get_infor(province = province_name,\
                            year = year,\
                            province_id = province_id,\
                            gaokao_type = gaokao_type,\
                            score_type = score_type)
                    time.sleep( random.randint(500,2000)/1000 ) # 随机暂停1到2秒



def get_infor(province, year, province_id, gaokao_type, score_type):
    """查询并保存某省份某一年的的高考一分一段

    Parameters
    ----------
    province_id : str
        查询的省份
    year : str
        查询的年份
    province_id : str
        查询的省份id
    gaokao_type : str
        高考类型,旧高考{1,2,3},新高考{2073,2074}
    score_type : str
        划线类型 {1,2,3}本科,专科,不区分
    """
    infor_url = f'https://static-data.gaokao.cn/www/2.0/section2021/{year}/{province_id}/{gaokao_type}/{score_type}/lists.json'
    p = path + f'\\province\\{province}'
    if not os.path.exists(p): # 文件夹是否存在
        os.makedirs(p) # 不存在就新键

    header = {
        'User-Agent': random.choice(u_a) # 随机挑选一个UA
    }

    response = requests.get(url = infor_url, headers = header)
    json_obj = response.json()

    if json_obj != '':
        fp = p + f'\\{year}_{province_id}_{gaokao_type}_{score_type}.json'
        fi = open(file = fp, mode = 'w', encoding = 'utf-8')
        json.dump(json_obj, fi, ensure_ascii = False)
        fi.close()
    else:
        pass
        


if __name__ == '__main__':
    # 首先读取省份的文件,根据数据形式组织查询结构
    # research()
    year = '2017'
    province_id = '31'
    gaokao_type = score_type = '3'
    infor_url = 'https://static-data.gaokao.cn/www/2.0/section2021/2017/31/3/3/lists.json'
    p = path + f'\\上海'
    if not os.path.exists(p): # 文件夹是否存在
        os.makedirs(p) # 不存在就新键

    header = {
        'User-Agent': random.choice(u_a) # 随机挑选一个UA
    }

    response = requests.get(url = infor_url, headers = header)
    json_obj = response.json()

    if json_obj != '':
        fp = p + f'\\{year}_{province_id}_{gaokao_type}_{score_type}.json'
        fi = open(file = fp, mode = 'w', encoding = 'utf-8')
        json.dump(json_obj, fi, ensure_ascii = False)
        fi.close()
    else:
        pass
    pass

