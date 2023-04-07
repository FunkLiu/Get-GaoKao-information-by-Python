import re

pattern = '学校id：(.+?),'
file_one = r'C:\Users\Lewis\Desktop\Demo\get school\error.txt'

file = open(file= file_one, mode='r', encoding= 'utf-8')
str_one = file.read()
file.close()

arr = re.findall(pattern, str_one)
print(arr)