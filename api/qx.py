# coding=utf-8
import urllib
import urllib.parse
import  requests
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
            i = i+1
            print('重新下载：'+url)

def getqxrules(subs,tags):             # 自定义规则
    
    try:
        rule = Retry_request('https://raw.githubusercontent.com/lzdnico/SSRClash/master/config/qxconfig')        #请求规则_神机规则
        rules = str(rule).split('下方粘贴你的订阅链接')
        subs = str(subs).split('@')
        tags = str(tags).split('@')
        for i in range(len(subs)):
            rules[0] += '\n' + subs[i] + ', tag=' +  tags[i] + ', enabled=true'
        return rules[0] + rules[1]
        
    except Exception as e:
        print(e)