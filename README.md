# 简介
  使用Python的requests库获取高考相关的信息，和高考微信小程序非常相关。
  该目录下有两个文件夹，分别是province和school，这两者功能分别是获取高考省份一分一段和每个高校信息。
  
# 预先准备
  province和school这两个文件夹下面有name.json和province.json，前者存储了高校的id和名称，后者存储了各个省份的id和名称，前者的接口忘记了，后者的接口是：
  [学校的id和名称](https://static-data.gaokao.cn/www/2.0/school/name.json)
  
# province介绍
  直接执行main.py文件，得到一分一段表，然后wash.py是后续处理用的，方便和小程序端的云开发平台对接
  
# school介绍
  ## 获取学校在各个省份的有效信息
    school_info_provience.py 以学校为中心，获取学校在各个省份的有效信息
    error_num_find.py 这个和前者对接，防止某些学校的信息没有获取到
    wash_information.py 处理获取得到的信息，整理成json文件方便上传到云开发平台
  
  ## 划分学校在各个省份的位置 
    divide_rank_and_fill_school.py 按照一定的处理规则进行学校的推荐
    
  ## 获取学校的logo
    get_school_logo.py 获取学校的logo
