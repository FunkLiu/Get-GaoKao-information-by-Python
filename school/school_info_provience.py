import requests
import json
import os
import sys
import random
import time
import copy
from math import ceil

# 多线程
import threading
from multiprocessing import Lock
from multiprocessing.dummy import Pool 

path = os.path.abspath(os.path.dirname(__file__))
u_a = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42']
start_time = time.time()
lock = Lock() # 声明线程锁
counter = 0

def id_to_name() -> dict:
    """读取存储省份名称和省份id的json文件,将解析为字典(dict)对象,解析过就直接返回字典(dict)对象,
    存储形式是
        {key:value} key:province_id, value:province_name
    """
    file_path = path + '\\id_to_name.json' # 需要保存的文件
    if not os.path.exists(file_path):     
        with open(file= path + '\\province.json', mode= 'r', encoding= 'utf-8') as file:
            dict_obj = dict(json.load(file))['data']['province']
            file.close()
        # 保存文件
        fi = open(file= file_path, mode= 'w', encoding= 'utf-8')
        json.dump(obj= dict_obj, fp= fi, ensure_ascii= False)
        fi.close()
    else:
        f = open(file= file_path, mode= 'r', encoding= 'utf-8')
        dict_obj = dict(json.load(f))
        f.close()

    #print(list(dict_obj.values()))
    #print(list(dict_obj.keys()))

    return dict_obj # 返回对象


def analysis_and_get():
    """分析对应文件夹下的json文件,同时得到有效的信息
    """
    # 读取文件,转化为dict对象
    file = open(path + '\\name.json', mode= 'r', encoding= 'utf-8')
    data = dict(json.load(file))['data'] # 需要的数据

    # 和前者是独立的
    analysis_dict = id_to_name()

    infor_arr = []
    check = set(['1916', '3379', '2949', '451', '1763', '3422', '3341', '3534', '3589', '3443'])

    for dic in data:
        if dic['proid'] not in analysis_dict: # 不在中国大陆的大学不记录
            continue
        if dic['school_id'] not in check:
            continue
        province = analysis_dict[dic['proid']]
        infor_arr.append({
            'province': province,
            'school_name': dic['name'],
            'school_id' : dic['school_id']
        })
    
    print(len(infor_arr))
    

    # 设置线程池
    pool = Pool(6)
    pool.map(pool_pass_infor, infor_arr) 
    pool.close() # 关闭进程池，关闭后po不再接收新的请求
    pool.join() # 等待po中所有子进程执行完成，必须放在close语句之后
    print('counter:',counter)
    return 

def pool_pass_infor(infor):
    global counter
    province,name,school_id = infor['province'],infor['school_name'],infor['school_id']
    try: 
        school_start_time = time.time()
        get_school_basic_infor(province, name, school_id)
        counter += 1
        t = time.time()
        now_time = time.ctime(t)
        cost_time = t - start_time
        print(f'{counter},当前时间:{now_time},该学校花费时间:{round(t - school_start_time,2)}秒,总共花费时间:{round(cost_time,2)}秒,爬取在{province}的{name}')
    except:
        t = time.time()
        now_time = time.ctime(t)
        cost_time = t - start_time
        print(f'!!!出现了问题,学校id：{school_id},当前时间:{now_time},总共花费时间:{round(cost_time,2)}秒,爬取在{province}的{name}')
        id = threading.current_thread().getName()
        with open(path + '\\' + 'error.txt', mode= 'a', encoding= 'utf-8') as f_error:
            lock.acquire()
            print(f'进程{id}将错误文件上锁')
            f_error.write(f'!!!出现了问题,学校id：{school_id},当前时间:{now_time},总共花费时间:{round(cost_time,2)}秒,爬取在{province}的{name}\n')
            f_error.close()
            lock.release()
        print(f'进程{id}将错误文件解锁')
    return 


def get_school_basic_infor(province, school_name, school_id):
    """根据学校的id获取学校的招生信息

    Parameters
    ----------
    province : str
        学校所在的省份
    school_name : str
        学校的名称
    school_id : str
        学校的id
    """
    # 配置文件
    url_config = f'https://static-data.gaokao.cn/www/2.0/school/{school_id}/dic/provincescore.json'
    path_config = path + '\\' + 'config' + '\\' + f'{province}'
    
    path_scoreLine = path + '\\' + 'scoreLine' + '\\' + f'{province}'
    path_schoolPlan = path + '\\' + 'schoolPlan' + '\\' + f'{province}'
    path_majorLine = path + '\\' + 'majorLine' + '\\' + f'{province}'
    
    path_arr = [path_config, path_scoreLine, path_schoolPlan, path_majorLine]
    for p in path_arr:
        if not os.path.exists(p):
            os.makedirs(p)
    
    # 首先获取学校在各个省份的配置信息
    header = {
        'User-Agent':random.choice(u_a) # 随机挑选一个UA
    }
    # 爬取
    response = requests.get(url= url_config, headers= header)
    json_obj = response.json()

    if json_obj != '': # 配置文件生成成功，考虑获取信息
        # 首先保存配置文件
        fp = path_config + f'\\{school_name}_{school_id}.json'
        file = open(file= fp, mode= 'w', encoding= 'utf-8')
        json.dump(obj= json_obj, fp= file, ensure_ascii= False)
        file.close()

        fp = path_scoreLine + f'\\{school_name}_{school_id}.json'
        file = open(file= fp, mode= 'w', encoding= 'utf-8')
        file.close()
        fp = path_schoolPlan+ f'\\{school_name}_{school_id}.json'
        file = open(file= fp, mode= 'w', encoding= 'utf-8')
        file.close()
        fp = path_majorLine + f'\\{school_name}_{school_id}.json'
        file = open(file= fp, mode= 'w', encoding= 'utf-8')
        file.close()

        # 然后根据配置文件获取有效信息，就可以获取后续的有效信息了
        useful_data = json_obj['data']['data']
        for check_dict in useful_data: # 遍历
            year = str(check_dict['year'])
            for province_dict in check_dict['province']:
                province_id = str(province_dict['pid'])
                type_arr = province_dict['type']
                batch_arr = province_dict['batch']
 
                # 首先获取分数线
                url_scoreLine = 'https://static-data.gaokao.cn/www/2.0/schoolprovinceindex/{year}/{school_id}/{province_id}/{line_type}/{page}.json'
                for line_type in type_arr:
                    header = {'User-Agent':random.choice(u_a)}
                    # 首先将页数定为1
                    response = requests.get(url= url_scoreLine.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), page= '1'), headers= header)
                    check_obj = response.json()
                    if check_obj != '':
                        arr = check_obj['data']['item']
                        # 获取页数
                        n = check_obj['data']['numFound']
                        pages_num = (n-n%10)//10 + int(not (n%10 == 0))
                        if pages_num > 1:
                            for pages in range(2, pages_num+1):
                                header = {'User-Agent':random.choice(u_a)}
                                response = requests.get(url= url_scoreLine.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), page= str(pages)), headers= header)
                                json_obj = response.json()
                                arr_new = json_obj['data']['item']
                                arr.extend(arr_new)
                        
                        # 保存
                        fp = path_scoreLine + f'\\{school_name}_{school_id}.json'
                        file = open(file= fp, mode= 'a', encoding= 'utf-8')
                        for ans in arr:
                            ans['year'] = year
                            json.dump(obj= ans, fp= file, ensure_ascii= False)
                        file.close()

                # 然后是招生计划和专业分数线
                url_schoolPlan = 'https://static-data.gaokao.cn/www/2.0/schoolplanindex/{year}/{school_id}/{province_id}/{line_type}/{batch}/{page}.json'
                url_majorLine = 'https://static-data.gaokao.cn/www/2.0/schoolspecialindex/{year}/{school_id}/{province_id}/{line_type}/{batch}/{page}.json'
                for line_type in type_arr:
                    for batch in batch_arr:
                        # 首先考虑招生计划
                        header = {'User-Agent':random.choice(u_a)}
                        # 首先将页数定为1
                        response_schoolPlan = requests.get(url= url_schoolPlan.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), batch= str(batch), page= '1'), headers= header)
                        check_obj = response_schoolPlan.json()
                        if check_obj != '':
                            arr = check_obj['data']['item']
                            # 获取页数
                            n = check_obj['data']['numFound']
                            pages_num = (n-n%10)//10 + int(not (n%10 == 0))
                            if pages_num > 1:
                                for pages in range(2, pages_num+1):
                                    header = {'User-Agent':random.choice(u_a)}
                                    response = requests.get(url= url_schoolPlan.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), batch= str(batch), page= str(pages)), headers= header)
                                    json_obj = response.json()
                                    arr_new = json_obj['data']['item']
                                    arr.extend(arr_new)
                            
                            # 保存
                            fp = path_schoolPlan+ f'\\{school_name}_{school_id}.json'
                            file = open(file= fp, mode= 'a', encoding= 'utf-8')
                            for ans in arr:
                                ans['year'] = year
                                json.dump(obj= ans, fp= file, ensure_ascii= False)
                            file.close()

                        # 然后是专业分数线
                        header = {'User-Agent':random.choice(u_a)}
                        # 首先将页数定为1
                        response_majorLine = requests.get(url= url_majorLine.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), batch= str(batch), page= '1'), headers= header)
                        check_obj = response_majorLine.json()
                        if check_obj != '':
                            arr = check_obj['data']['item']
                            # 获取页数
                            n = check_obj['data']['numFound']
                            pages_num = (n-n%10)//10 + int(not (n%10 == 0))
                            if pages_num > 1:
                                for pages in range(2, pages_num+1):
                                    header = {'User-Agent':random.choice(u_a)}
                                    response = requests.get(url= url_majorLine.format(year= year, school_id= school_id, province_id= province_id, line_type= str(line_type), batch= str(batch), page= str(pages)), headers= header)
                                    json_obj = response.json()
                                    arr_new = json_obj['data']['item']
                                    arr.extend(arr_new)
                            
                            # 保存
                            fp = path_majorLine + f'\\{school_name}_{school_id}.json'
                            file = open(file= fp, mode= 'a', encoding= 'utf-8')
                            for ans in arr:
                                ans['year'] = year
                                json.dump(obj= ans, fp= file, ensure_ascii= False)
                            file.close()

        time.sleep( random.randint(250, 500)/1000 ) # 休息间隔
    else:
        time.sleep( random.randint(100, 500)/1000 )
        pass
    

if __name__ == '__main__':
    print('开始爬取')
    analysis_and_get()
    print('爬取结束')
    
    # f = open(path + '\\province.json', 'r', encoding= 'utf-8')
    # dict_obj = dict(json.load(f))
    # f.close()
    # f = open(path + '\\province.json', 'w', encoding= 'utf-8')
    # json.dump(dict_obj, f, ensure_ascii= False)
    # f.close()
    pass