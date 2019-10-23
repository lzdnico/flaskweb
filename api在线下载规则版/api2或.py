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


def safe_base64_decode(s): # 解码
    try:
        if len(s) % 4 != 0:
            s = s + '=' * (4 - len(s) % 4)
        base64_str = base64.urlsafe_b64decode(s)
        return bytes.decode(base64_str)
    except Exception as e:
        print('解码错误')###

def safe_base64_encode(s): # 加密
    try:
        return base64.urlsafe_b64encode(bytes(s, encoding='utf8'))
    except Exception as e:
        print('解码错误',e)

def Retry_request(url): #超时重传
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

def getnodeR(s):             #获取节点信息

    config = {
    "remark": "",
    "server": "0.0.0.0",
    "server_port": 8388,
    "password": "m",
    "method": "aes-128-ctr",
    "protocol": "auth_aes128_md5",
    "protocol_param": "",
    "obfs": "tls1.2_ticket_auth_compatible",
    "obfs_param": ""
    }

    #s = safe_base64_decode(ssr)
    spilted = re.split(':',s)  #将多个参数分离开来
    pass_param = spilted[5]
    pass_param_spilted = re.split('\/\?',pass_param)
    passwd = safe_base64_decode(pass_param_spilted[0]) #解码得到password
    try:
        obfs_param = re.search(r'obfsparam=([^&]+)',pass_param_spilted[1]).group(1)
    except:
        obfs_param=""
    try:
        protocol_param = re.search(r'protoparam=([^&]+)', pass_param_spilted[1]).group(1)
        protocol_param = safe_base64_decode(protocol_param)
    except:
        protocol_param = ''
    try:
        remarks = re.search(r'remarks=([^&]+)', pass_param_spilted[1]).group(1)
        remarks = safe_base64_decode(remarks)
    except:
        remarks = '' 

    config['remark'] = remarks
    config['server'] = spilted[0]
    config['server_port'] = int(spilted[1])
    config['password'] = passwd
    config['method'] = spilted[3]
    config['protocol'] = spilted[2]
    config['obfs'] = spilted[4]
    config['protocol_param'] = protocol_param
    config['obfs_param'] = obfs_param

    return config

def getrules():             # 自定义规则
    
    finalrules=[]
    rules = Retry_request('https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/Pro.yaml')        #请求规则_神机规则
    p_rule= Retry_request('https://raw.githubusercontent.com/lzdnico/ToClash/master/General.yml')               #基础规则_默认不配置DNS
    #p_rule=rules.split('Proxy:')[0]                                                                            #基础规则_默认配置DNS,与上面二选一
    l_rule =  rules.split('Rule:\n')[1].replace('ForeignMedia','国际媒体').replace('DomesticMedia','国内媒体').replace('Hijacking','恶意网站').replace('Final','漏网之鱼').replace('PROXY','代理模式')
    nf_rule = l_rule.split('# > Netflix\n')[1].split('# > PBS\n')[0].replace('国际媒体','Netflix')
    l_rule = nf_rule+l_rule
    Peoxies = 'Proxy:\n'
    finalrules.append(p_rule)
    finalrules.append(Peoxies)
    finalrules.append(l_rule)
    return finalrules

def writeRules(sublink):    #返回策略组及规则
    try:
        other=[]
        name =''        
        Peoxies = ''
        rules = getrules
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        #ssrdata = data.strip().replace('==','').split('\n')            
        for i in range(len(ssrdata)):                                                   #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '':
                if nodeR['method'] == 'none':
                    continue
                Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
            else:
                Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                  'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
            Peoxies +='- '+str(Json)+'\n'
            other.insert(0,remark)
        proxy = str(other)
        proxy1 = proxy[1:-1]
        ProxyGroup='\n\nProxy Group:\n\n'\
                '- { name: "代理模式", type: select, proxies: [ "故障切换","手动选择","延迟最低","DIRECT"] }\n'\
                '- { name: "延迟最低", type: "url-test", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 600'+ '}\n'\
                '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 600'+ '}\n'\
                '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                'Rule:\n'
        rules = getrules()        
        currenttime = '# 更新时间为（看分钟就行，不知道哪个时区）：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        content = currenttime+rules[0]+rules[1]+Peoxies+ProxyGroup+rules[2]
        return content

    except Exception as e:
            print('返回规则错误')
            return 'STC可用，注册地址：bilibili.stcservers.com/auth/register?code=gzI5'


def getcustomssrlink(sublink, flagname):    #返回策略组及规则
    try:
        other=[]     
        customssr = ''  
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')           
        for i in range(len(ssrdata)):                                                   #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            for flag in flags: 
                if flag == '' :
                    continue
                if  flag in remark:
                    customssr += ssrdata[i]+'\n'
        customssr = safe_base64_encode(customssr)
        return customssr
    except Exception as e:
            print('客制化ssr订阅错误',e)
            return 'STC可用，注册地址：http://best.stcservers.com/auth/register?code=gzI5'
def writeRulescustom(sublink,flagname):    #返回策略组及规则
    try:
        other=[]
        name =''        
        Peoxies = ''
        rules = getrules
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')
        #ssrdata = data.strip().replace('==','').split('\n')            
        for i in range(len(ssrdata)):                                                   #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            for flag in flags:
                if flag == '':
                    continue
                if flag in remark:
                    if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '':
                        if nodeR['method'] == 'none':
                            continue
                        Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                        'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
                    else:
                        Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                        'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
                    Peoxies +='- '+str(Json)+'\n'
                    other.insert(0,remark)
                else:
                    continue

        proxy = str(other)
        proxy1 = proxy[1:-1]
        ProxyGroup='\n\nProxy Group:\n\n'\
                '- { name: "代理模式", type: select, proxies: [ "故障切换","手动选择","延迟最低","DIRECT"] }\n'\
                '- { name: "延迟最低", type: "url-test", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 600'+ '}\n'\
                '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 600'+ '}\n'\
                '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                'Rule:\n'
        rules = getrules()        
        currenttime = '# 更新时间为（看分钟就行，不知道哪个时区）：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        content = currenttime+rules[0]+rules[1]+Peoxies+ProxyGroup+rules[2]
        return content

    except Exception as e:
            print('返回客制化规则错误')
            return 'STC可用，注册地址：bilibili.stcservers.com/auth/register?code=gzI5'
app = Flask(__name__)

@app.route('/')
def my():
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text=no_ssrlink')
    return '你的订阅地址呢。Kris最棒！！！'

@app.route('/NicoNewBeee/rui')
def rui():
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text=she_see_me')
    text = Retry_request('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/getupdates')
    return str(text).split('/she')[-1].split('"')[0]

@app.route('/ssr/<name>',methods=['GET'])
def ssrlink(name):
    flags = name.split('@')
    url = flags[0].replace('!','/')
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了你的ssr_api:'+url))
    custom = ''
    for i in range(len(flags)):
        if i == 0:
            continue
        custom += flags[i]+'@'
        
    if 'stc' in url or 'z2o.fun' in url or 'qcrane' in url :
        return getcustomssrlink(url,custom)
    else :
        return 'STC可用，注册地址：bilibili.stcservers.com/auth/register?code=gzI5'

@app.route('/<name>',methods=['GET'])
def get(name):
    name = name.replace('!','/')
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了你的api:'+name))
    if '@' in name:
        customclash = name.split('@')
        url = customclash[0]
        custom = ''
        for i in range(len(customclash)):
            if i == 0:
                continue
            custom += customclash[i]+'@' 
        if 'stc' in url or 'z2o.fun' in url or 'qcrane' in url :
            return writeRulescustom(url,custom)
        else :
            return 'STC可用，注册地址：bilibili.stcservers.com/auth/register?code=gzI5'         
    elif 'stc' in name or 'z2o.fun' in name or 'qcrane' in name :
        return writeRules(name)
    else :
        return 'STC可用，注册地址：bilibili.stcservers.com/auth/register?code=gzI5'
    
#https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text=iloveyou
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=10086)