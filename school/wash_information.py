from multiprocessing.dummy import Pool
import os 
import json 
import re
from school_info_provience import id_to_name

path = os.path.abspath(os.path.dirname(__file__))
analysis_dict = id_to_name() # 指示学校id和学校名称的对应关系，可以用来排除非大陆的学校
right_set = set(['63'])
less_arr = []
all_less = []

def wash_one(file_path:str, school_id:str):
    """处理某个学校下的特定数据,根据file_path指定打开文件"""
    try:
        fp = open(file_path, mode= 'r', encoding= 'utf-8')
        str_read = fp.read()
        fp.close()
    except:
        print(f'打开文件出错,文件为{file_path}')
        return False
    
    pattern_find = '(\{.+?\})'
    data_arr = re.findall(pattern= pattern_find, string= str_read)

    dict_write = {}
    dict_write['school_id'] = school_id
    dict_write['data'] = dict()
    # if len(data_arr) <= 1:
    #     print(f'太少了，疑似爬取失败{file_path}')
    #     less_arr.append(school_id)
    #     return False
    for data in data_arr:
        try:
            data = data.replace('null','\'\'') # 替换掉null
            data = eval(data)
        except:
            print(f'eval函数出错,文件为{file_path}')
            return False
        for pid in ['province_id','pid','proid','province']: # 由于数据里面确定年份有好几种类型，所以必须这样
            if pid in data:
                ans_province_id = data[pid]
                break

        ans_year, ans_type, ans_batch = data['year'], data['type'], data['batch']
        del data['year']
        del data[pid]
        del data['school_id']

        # 多级字典写入
        if ans_year not in dict_write['data']:
            dict_write['data'][ans_year] = {}
        if ans_province_id not in dict_write['data'][ans_year]:
            dict_write['data'][ans_year][ans_province_id] = {}
        if f'{ans_type}_{ans_batch}' not in dict_write['data'][ans_year][ans_province_id]:
            dict_write['data'][ans_year][ans_province_id][f'{ans_type}_{ans_batch}'] = {}
        dict_write['data'][ans_year][ans_province_id][f'{ans_type}_{ans_batch}'] = data
    # 写入
    fp = open(file_path, mode= 'w', encoding= 'utf-8')
    json.dump(dict_write, fp, ensure_ascii= False)
    fp.close()

    return True


def wash_infor(name_dict):
    """处理学校的所有数据"""
    try:
        school_id = name_dict['school_id']
        school_name = name_dict['school_name']
        province_id = name_dict['province_id']
        file_name = f'{school_name}_{school_id}.json' # 都是这样保存的
    except:
        print(name_dict)
        print('字典对象错误')
        return
    # 获取学校的省份，同时给出各个路径
    province = analysis_dict[province_id]
    path_scoreLine = path + '\\' + 'scoreLine' + '\\' + f'{province}'
    path_schoolPlan = path + '\\' + 'schoolPlan' + '\\' + f'{province}'
    path_majorLine = path + '\\' + 'majorLine' + '\\' + f'{province}'    
    
    # 依次处理各类信息
    print(f'school_id:{school_id},name:{school_name}')
    right_set.add(school_id)
    for p in [ path_schoolPlan, path_majorLine]:
        try:
            wash_one(file_path= p + '\\' + file_name, school_id= school_id)
        except:
            print('其他错误')
            right_set.remove(school_id)
            break
    
        
    
if __name__ == '__main__':
    
    # 打开name.json找到需要的学校
    iter_file = open(path + '\\' + 'name.json', mode= 'r', encoding= 'utf-8')
    inter_arr = dict(json.load(iter_file))['data']
    iter_file.close()
    infor_arr = []

    check = set(['1916', '3379', '2949', '451', '1763', '3422', '3341', '3534', '3589', '3443'])

    for dic in inter_arr:
        if dic['proid'] not in analysis_dict: # 不在中国大陆的大学不记录
            continue
        if dic['school_id'] not in check: # 成功的学校跳过
            continue 
        province = analysis_dict[dic['proid']]
        infor_arr.append({
            'province_id': dic['proid'],
            'school_name': dic['name'],
            'school_id' : dic['school_id']
        })

    print(len(infor_arr))

    pool = Pool(6)
    pool.map(wash_infor, infor_arr)
    pool.close() # 关闭线程池
    pool.join()

    all_less.extend(less_arr)


    # 设置线程
    dis = 100
    for i in range(1200,len(infor_arr),dis):
        print(f'!!!{i}!!!')
        pool = Pool(6)
        pool.map(wash_infor, infor_arr[i: i+dis])
        pool.close() # 关闭线程池
        pool.join()

        f = open(path+'\\'+'error_arr.txt',mode= 'a', encoding= 'utf-8')
        f.write(f'太少了：{i}:{i+dis} == {str(less_arr)}\n')
        all_less.extend(less_arr)
        less_arr.clear()
        f.close()

    print('end')
 

