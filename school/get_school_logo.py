import requests 
import random
import os
import json

path = os.path.abspath(os.path.dirname(__file__))
u_a = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42']
pic_file_format_arr = ['jpg', 'bmp', 'jpeg', 'png', 'tif', 'gif'] # 常见的图片格式
logo_path = path+ '/school_logo'
if not os.path.exists(logo_path):
    os.makedirs(logo_path)

def get_school_logo(school_id):
    
    url = 'https://static-data.gaokao.cn/upload/logo/{school_id}.{pic_file_format}'

    for pic_file_format in pic_file_format_arr: # 遍历文件格式
        # 首先获取学校在各个省份的配置信息
        header = {
            'User-Agent':random.choice(u_a) # 随机挑选一个UA
        }
        # 爬取
        target_url = url.format(school_id = school_id, pic_file_format= pic_file_format)
        response = requests.get(url= target_url, headers= header)
        if response.ok : # 获取成功
            file_name = f'{school_id}.{pic_file_format}'
            fp = open(logo_path+ f'/{file_name}', mode= 'wb')
            fp.write(response.content)
            fp.close()
            break

        
if __name__ == '__main__':
    with open(path+ '/name.json', mode= 'r', encoding= 'utf-8') as fp:
        school_arr = list(json.load(fp)['data'])
        fp.close()
    for i,school in enumerate(school_arr):
        school_id = school['school_id']
        name = school['name']
        print(f'{i} {name}')
        get_school_logo(school_id)

