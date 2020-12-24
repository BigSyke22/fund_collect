import json
import re
import requests



'''
通过基金编码获取估值
'''
code = '005827'
url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
result = requests.get(url)  # 发送请求
data = json.loads(re.match(".*?({.*}).*", result.text, re.S).group(1))
print('##############基金详情##############')
print('基金编码：%s' % data['fundcode'])
print('基金名称：%s' % data['name'])
print('单位净值：%s' % data['dwjz'])
print('净值日期：%s' % data['jzrq'])
print('估算值：%s' % data['gsz'])
print('估算增量：%s%%' % data['gszzl'])
print('估值时间：%s' % data['gztime'])