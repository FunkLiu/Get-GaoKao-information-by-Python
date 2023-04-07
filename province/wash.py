import os
import sys
import json
import requests
import collections

flod = os.path.abspath(os.path.dirname(__file__))

def re_write(dir_name, file_name:str):
    # 打开文件
    file_name = file_name.replace('.json', '')
    year, province_id, type, line_type = file_name.split('_')
    with open(dir_name, mode= 'r', encoding= 'utf-8') as file:
        json_obj = json.load(file)
        for key in ['code','message','md5']:
            del json_obj[key]
        # 添加键值对
        json_obj['year'] = year
        json_obj['province_id'] = province_id
        json_obj['type'] = type
        json_obj['line_type'] = line_type
        file.close()
    with open(dir_name, mode= 'w', encoding= 'utf-8') as file:
        json.dump(json_obj, fp= file, ensure_ascii= False)
        file.close()
    print(dir_name)
        

def wash():
    # 首先当前文件夹        
    for fl in os.listdir(flod):
        if os.path.isdir(flod + f'\\{fl}'):
            for file_name in os.listdir(flod + f'\\{fl}'):
                f = flod + f'\\{fl}' + f'\\{file_name}'
                if os.path.isfile(f):
                    re_write(f, file_name)

def explain():
    file = open(flod + '\\all.json', mode= 'w', encoding= 'utf-8')
    for fl in os.listdir(flod):
        if os.path.isdir(flod + f'\\{fl}'):
            for file_name in os.listdir(flod + f'\\{fl}'):
                f = flod + f'\\{fl}' + f'\\{file_name}'
                if os.path.isfile(f):
                    new_line = open(f, mode= 'r', encoding= 'utf-8')
                    file.write(new_line.read() + '\n')
                    new_line.close()
    file.close()
                    
def get_max_number(): # 获取每个省份的高考人数
    save_dict = collections.defaultdict(list)
    flod_stack = [flod + '/province']
    while flod_stack:
        node = flod_stack.pop()
        for ans in os.listdir(node):
            new_dir = node + f'/{ans}'
            if os.path.isdir(new_dir):
                flod_stack.append(new_dir)
            else:
                arr = ans.split("_")
                fp = open(new_dir, mode='r', encoding= 'utf-8')
                dict_obj = dict(json.load(fp))
                ele = dict_obj['data']['list'][-1]
                total_num = int(ele['total'])

                del dict_obj['data']
                dict_obj['total_num'] = total_num
                save_dict[arr[1]].append(dict_obj)
                    
                fp.close()
                pass
    
    for k in save_dict.keys():
        save_dict[k].sort(key= lambda x:int(x['year']), reverse= True)

    save_dir = flod + '/num_in_gaokao.json'
    fp = open(save_dir, mode= 'w', encoding= 'utf-8')
    json.dump(save_dict, fp= fp, ensure_ascii= False)
    fp.close()
    return 
                    


if __name__ == '__main__':
    get_max_number()
    # wash()
    #explain()
    pass
