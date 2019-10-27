# coding=utf-8
import sys
from flask import Flask, request
import flask_restful
import  base64
import  re
import  requests
import urllib3
import urllib
import urllib.parse
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

def getrules(subs,tags):             # 自定义规则
    
    try:
        rule = Retry_request('https://raw.githubusercontent.com/lzdnico/SSRClash/master/loonconfig')        #请求规则_神机规则
        rules = str(rule).split('# 在[server_remote] 下方粘贴你的订阅链接')
        proxy = rules[1].split('# API标志位1')
        tag = ''
        subs = str(subs).split('@')
        tags = str(tags).split('@')

        for i in range(len(subs)):
            try:
                link = subs[i].split('regex=')[0]
                filte = 'regex='+ urllib.parse.quote(subs[i].split('regex=')[1])
                subs[i] = link+filte
            except Exception as e:
                pass
            rules[0] += '\n' + tags[i] +  '=' + subs[i]
            tag += ', '+ tags[i]
        proxy[0] += '\n' + 'PROXY = select,ss' +tag
        return rules[0] + proxy[0] + proxy[1]
        
    except Exception as e:
        return '检测格式'

app = Flask(__name__)

@app.route('/')
def my():
    return 'qx api 使用：<br/>调用地址为：http://ip:10087/订阅地址@tag。其中订阅地址中的&替换为!，tag为标签<br/>'\
            '将调用地址复制到qx——配置文件——下载。<br/>'\
            '保存后，长按策略图标，给健康检测添加节点。将最优的节点排在前面。<br/>'

    
@app.route('/loon', methods=['GET', 'POST'])
def search():
    try:
        sub = request.args.get('sublink').replace('!','&')              
        print(sub)
        tag=request.args.get('tag')
        print(tag)
        return  getrules(sub,tag)

    except Exception as e:
        return '请调用格式适合正确'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=10087)