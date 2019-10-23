# coding=utf-8
import sys
import flask_restful
from flask import Flask
import  base64
import  re
import  requests
import urllib3
import json
import time
from flask import render_template
from flask import request
urllib3.disable_warnings()
aff = 'STC可用，注册地址：prohub.stchks.com/auth/register?code=gzI5'


def safe_base64_decode(s): # 解码
    try:
        if len(s) % 4 != 0:
            s = s + '=' * (4 - len(s) % 4)
        base64_str = base64.urlsafe_b64decode(s)
        return bytes.decode(base64_str)
    except Exception as e:
        print('解码错误')   

def safe_base64_encode(s): # 加密
    try:
        return base64.urlsafe_b64encode(bytes(s, encoding='utf8'))
    except Exception as e:
        print('解码错误',e)

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
    
    try:
        finalrules=[]
        
        with open("./general.yml", "r",encoding = 'utf-8') as f:
            p_rule = f.read() + '\n'

        with open("./lrules.yml", "r",encoding = 'utf-8') as f:
            l_rule = f.read()        
        
        Peoxies = 'Proxy:\n'
        finalrules.append(p_rule)
        finalrules.append(Peoxies)
        finalrules.append(l_rule)
        return finalrules
    except Exception as e:
        print(e)

def writeRules(sublink,selectfirst):    #策略组及规则
    try:
        other=[]           #节点名list           
        Peoxies = ''       #节点
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')              
        for i in range(len(ssrdata)):                                                   #遍历节点            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '':    #判断是否为ssr
                if nodeR['method'] == 'none':
                    continue
                Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
            else:
                Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                  'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
            Peoxies +='- '+str(Json)+'\n'    #节点加加
            other.insert(0,remark)           #节点名list加加
        proxy = str(other)                   #节点名转化为字符串
        proxy1 = proxy[1:-1]                 #节点名字符串去掉中括号
        #'- { name: "延迟最低", type: "url-test", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 600'+ '}\n'\
        if selectfirst == 'yes':             #是否修改代理模式默认顺序，默认为故障切换在前
            ProxyGroup='\n\nProxy Group:\n\n'\
                    '- { name: "代理模式", type: select, proxies: ["手动选择","故障切换","负载均衡","DIRECT"] }\n'\
                    '- { name: "负载均衡", type: "load-balance", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                    '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                    '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                    '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                    'Rule:\n'
        else :
            ProxyGroup='\n\nProxy Group:\n\n'\
                    '- { name: "代理模式", type: select, proxies: [ "故障切换","手动选择","负载均衡","DIRECT"] }\n'\
                    '- { name: "负载均衡", type: "load-balance", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                    '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                    '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                    '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                    'Rule:\n'           
        rules = getrules()   #获取分流规则       
        currenttime = '# 更新时间为（看分钟就行，不知道哪个时区）：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n' #获取更新时间
        content = currenttime+rules[0]+rules[1]+Peoxies+ProxyGroup+rules[2]
        return content

    except Exception as e:
            print (e)
            return aff

def getcustomssrlink(sublink, flagname):    #客制化ssr订阅
    try:   
        customssr = ''     #客制化节点组
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')     #拆分    
        for i in range(len(ssrdata)):    #遍历所有节点                                                 
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:        #用于剔除高倍率节点
                continue
            for flag in flags:          #遍历节点匹配
                if flag == '' :         #滤掉无效匹配请求
                    continue
                if  flag.split('&')[0] in remark:   #节点是否匹配
                    if '&' in flag:                 #是否有与操作符
                        inremark = 1                #标志位，一组里有一个不匹配就为0，就不匹配
                        andflags = flag.split('&')  #拆分一组的多个匹配规则  @香港&1倍@美国     香港&1倍 为一组
                        for andflag in andflags:
                            if andflag == '':       #滤掉无效匹配请求
                                continue
                            else:
                                if andflag in remark:
                                    inremark = inremark * 1
                                else:
                                    inremark = 0  
                        if inremark == 1:           #标志位是否为1                      
                            customssr += ssrdata[i]+'\n'
                    else:                         #没有与操作符  
                        customssr += ssrdata[i]+'\n'
        customssr = safe_base64_encode(customssr)   #base64加密
        return customssr
    except Exception as e:
            return aff

def writeRulescustom(sublink,flagname,selectfirst):    #客制化策略组及规则
    try:
        other=[]       
        Peoxies = ''
        noderemark = ''      #用于剔除节点标准
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')
        #ssrdata = data.strip().replace('==','').split('\n')            
        for i in range(len(ssrdata)):          #遍历节点                                         #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            for flag in flags:     #遍历分组匹配规则
                if flag == '':
                    continue
                if flag.split('&')[0] in remark:   #每组第一个匹配
                    if '&' in flag:                #每组是否有多个匹配要求   @香港&1倍@美国     适用 香港&1倍  
                        inremark = 1
                        andflags = flag.split('&')
                        for andflag in andflags:
                            if andflag == '':
                                continue
                            else:
                                if andflag in remark:
                                    inremark = inremark * 1
                                else:
                                    inremark = 0
                        if inremark == 1:
                            if remark in noderemark:
                                continue
                            else:
                                Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                                'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
                                noderemark += remark
                                Peoxies +='- '+str(Json)+'\n'
                                other.insert(0,remark)
                        else :
                            continue
                    else :                         #每组是否有多个匹配要求   @香港&1倍@美国     适用 美国这组
                        if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '':
                            if nodeR['method'] == 'none':
                                continue
                            Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                            'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
                            Peoxies +='- '+str(Json)+'\n'
                            other.insert(0,remark)
                        else:
                            if remark in noderemark:
                                continue
                            else:
                                Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                                'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
                                noderemark += remark
                                Peoxies +='- '+str(Json)+'\n'
                                other.insert(0,remark)
                else:                              #每组第一个不匹配
                    continue

        proxy = str(other)
        proxy1 = proxy[1:-1]
        if selectfirst == 'yes':
            ProxyGroup='\n\nProxy Group:\n\n'\
                    '- { name: "代理模式", type: select, proxies: ["手动选择","故障切换","负载均衡","DIRECT"] }\n'\
                    '- { name: "负载均衡", type: "load-balance", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                    '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                    '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                    '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                    'Rule:\n'
        else :
            ProxyGroup='\n\nProxy Group:\n\n'\
                    '- { name: "代理模式", type: select, proxies: [ "故障切换","手动选择","负载均衡","DIRECT"] }\n'\
                    '- { name: "负载均衡", type: "load-balance", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
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
            return aff

app = Flask(__name__)

@app.route('/NicoNewBeee/rui')
def rui():
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text=she_see_me')
    text = Retry_request('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/getupdates')
    return str(text).split('/she')[-1].split('"')[0]

@app.route('/ssr/<name>',methods=['GET'])
def ssrlink(name):
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了你的SSR_API : \n'+name.replace('!','/')))
    flags = name.split('@')
    url = flags[0].replace('!','/')
    custom = ''
    for i in range(len(flags)):
        if i == 0:
            continue
        custom += flags[i]+'@'
        
    if 'stc' in url or 'z2o.fun' in url or 'qcrane' in url :
        return getcustomssrlink(url,custom)
    else :
        return aff

@app.route('/clash/<name>',methods=['GET'])
def get(name):
    name = name.replace('!','/')
    requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了你的Clash_API : \n'+name))
    try:
        selectfirst = name.split('@@')[1]
    except Exception as e:
        selectfirst = 'no'
    name = name.split('@@')[0]
    if '@' in name:
        customclash = name.split('@')
        url = customclash[0]
        custom = ''
        for i in range(len(customclash)):
            if i == 0:
                continue
            custom += customclash[i]+'@' 
        if 'stc' in url or 'z2o.fun' in url or 'qcrane' in url :
            return writeRulescustom(url,custom,selectfirst)
        else :
            return aff     
    elif 'stc' in name or 'z2o.fun' in name or 'qcrane' in name :
        return writeRules(name,selectfirst)
    else :
        return aff
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人打开了你的托管页面 : \n'))
        sub = request.form['left']
        Clash = 'http://185.238.248.145:10086/clash/'+str(sub).replace('/','!')
        QX = 'http://185.238.248.145:2333/'+str(sub).replace('/','!')+'@STC'
        return render_template('index.html', Clash = str(Clash),QX = str(QX))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=10086)