# 会产生一个json文件，这个文件会将每个省份的id作为key
# 然后value为一个list
# 每一个list的元素是一个dict，
# 其中有两个key，对应的是type和data，
# data里面是一个第二维度可变的二维数组，数组长度为(100/0.1) = 1000

import json
import os
import collections

path = os.path.dirname(os.path.abspath(__file__))
arr_length = 1000 # 定义数组长度
score_path = path + '/scoreLine'
province_special_arr = ['11', '12', '31']
with open(path + '/num_in_gaokao.json', mode= 'r', encoding= 'utf-8') as fp:
    dict_num = dict(json.load(fp)) 
    fp.close()


def offset_func(x:float, p=3):# 设置一个凸函数y = a*x**(1/p) + b （a，b，p是系数，p是正整数）
    # 因为经过(0,0,002)和(1,0.02)这两点，所以是这样的
    return 0.018*(x)**(1/p) + 0.002
    

def write_dict(dict_obj:dict, p:str):
    try:
        with open(p, mode= 'r', encoding= 'utf-8') as fp:
            dict_load = dict(json.load(fp))
            school_id = dict_load['school_id']
            data = dict_load['data']
            fp.close()   
        for year in range(2022, 2010, -1):
            if str(year) in data:
                infor = dict(data[str(year)])
                break
    except:
        print('出问题啦！！！')
        return 

    def filt(receive_dict:dict, province_flag= False):
        ret = []
        for k in receive_dict.keys():
            type_set = set()
            if (province_flag or "专科批" not in receive_dict[k]['local_batch_name']):
                province_flag =  False
            if receive_dict[k]["zslx_name"] == '普通类' and receive_dict[k]['type'] not in type_set :
                ele = {
                    'type' : receive_dict[k]['type'],
                    'min_section' : receive_dict[k]['min_section']
                }
                type_set.add(receive_dict[k]['type'])
                ret.append(ele)
        return ret, province_flag

    check_deque = collections.deque([k for k in infor.keys()])
    per_situation = None
    situation_arr = []
    counter = len(check_deque)
    while check_deque: # 这里的k是省份的id
        k = check_deque.popleft() # 从队列最左侧出来元素
        province_flag = k not in province_special_arr
        res, continue_flag = filt(infor[k], province_flag)
        if k not in dict_obj: # 这个省份还没有出现
            dict_obj[k] = [{'type': ele['type'], 'data':[[] for i in range(arr_length)]} for ele in res] # 初始化保存列表
        if (k not in dict_num or continue_flag) :
            if not check_deque:
                break 
            else:
                continue
        province_num_arr = dict_num[k]
        for ele in res :
            min_section = ele['min_section']
            min_section = int(min_section)
            if min_section == 0 and per_situation is None: # 没有找到好的per_situation
                check_deque.append(k) # 重新归到队列右侧
                break
            for ans in province_num_arr: # 找该省份的不同高考类型的人数
                if ans['type'] == ele['type']:
                    if min_section != 0 : # 计算所处位置
                        situation = min_section/ans['total_num']  
                        situation_arr.append(situation)
                    else: 
                        situation = per_situation 
                    offset = offset_func(situation) # 计算偏移量                        
                    for index_f in range(len(dict_obj[k])): # 寻找保存列表的索引
                        if  dict_obj[k][index_f]['type'] == ele['type']:  
                            start = (situation - offset) * arr_length if situation-offset>0 else 0
                            end = (situation + offset*0.8) * arr_length # 这里可以稍微减少一点下界
                            for i in range(int(start), int(min(arr_length, end))):
                                dict_obj[k][index_f]['data'][i].append(school_id) 
                            if 'total_num' not in dict_obj[k][index_f]:
                                dict_obj[k][index_f]['total_num'] = ans['total_num']
                            if ele['min_section'] != '0':
                                per_situation = situation
                            break 
                    break
        counter -= 1
        if counter < 0:
            break
        
    if len(situation_arr) == 0:
        return 
    situation_aver = sum(situation_arr)/len(situation_arr) # 计算均值
    for k in (province_special_arr + list(check_deque)): # 特别省份的单独用均值
        if k not in dict_obj:
            continue
        for index_f in range(len(dict_obj[k])): # 寻找保存列表的索引
            if  dict_obj[k][index_f]['type'] == ele['type']:  
                start = (situation_aver - offset) * arr_length if situation_aver-offset>0 else 0
                end = (situation_aver + offset) * arr_length
                for i in range(int(start), int(min(arr_length, end))):
                    dict_obj[k][index_f]['data'][i].append(school_id) 
                break


def main():
    d = collections.deque()
    d.append(score_path)
    save_dict = {}
    counter = 0
    while d:
        node = d.popleft()
        for ans in os.listdir(node):
            new_path = node + f'/{ans}'
            if os.path.isdir(new_path):
                d.append(new_path)
            elif os.path.isfile(new_path) and new_path[-4:] == 'json':
                print(f'{counter} {ans}')
                write_dict(save_dict, new_path)
                counter += 1
            else:
                pass
    fp = open(path + '/province_school_select.json', mode= 'w', encoding= 'utf-8')
    for k in save_dict.keys():    
        json.dump( {'province_id':k, 'data' : save_dict[k]}, fp, ensure_ascii= False)
    fp.close()

    # 因为数据库查询的原因，所以还要修改一下获取高考人数的json文件
    new_file_dir = path + '/num_in_gaokao_upload.json'
    fp = open(new_file_dir, mode= 'w', encoding= 'utf-8')
    for k in dict_num:
        json.dump({'province_id':k, 'data' : dict_num[k]}, fp, ensure_ascii= False)
    fp.close()



if __name__ == '__main__':
    main()

