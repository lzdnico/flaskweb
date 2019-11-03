# coding=utf-8
import sys
import  base64
import  re
import  requests
import urllib3
import urllib
import urllib.parse
import json
import time
urllib3.disable_warnings()

#全局变量定义
aff = 'STC可用，注册地址：bilibili.stchk.cloud/auth/register?code=gzI5'

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
        
        with open("./config/general.yml", "r",encoding = 'utf-8') as f:
            p_rule = f.read() + '\n'

        with open("./config/lrules.yml", "r",encoding = 'utf-8') as f:
            l_rule = f.read()        
        
        Peoxies = 'Proxy:\n'
        finalrules.append(p_rule)
        finalrules.append(Peoxies)
        finalrules.append(l_rule)
        return finalrules
    except Exception as e:
        print(e)

def writeRulescustom(sublink,flagname,selectfirst):    #客制化策略组及规则
    try:
        #print(sublink + 'custom')
        other=[]       
        Peoxies = ''
        noderemark = ''      #用于剔除节点标准
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')
        #ssrdata = data.strip().replace('==','').split('\n') 
        
    
        groups = [[] for _ in range(len(flags))]
        print(groups)

        for i in range(len(ssrdata)):          #遍历节点                                         #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']                                
            
            if "30倍" in remark:  #用于剔除高倍率节点
                continue
            
            for i in range(len(flags)):     #遍历分组匹配规则
                if flags[i] == '':
                    continue
                if flags[i].split('&')[0] in remark:   #每组第一个匹配
                    if '&' in flags[i]:                #每组是否有多个匹配要求   @香港&1倍@美国     适用 香港&1倍  
                        inremark = 1
                        andflags = flags[i].split('&')
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
                                if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '' and nodeR['protocol'] == 'origin' and nodeR['obfs'] == 'plain':    #判断是否为ssr
                                    if nodeR['method'] == 'none':
                                        continue
                                    Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                                    'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
                                    Peoxies +='- '+str(Json)+'\n'
                                    groups[i].insert(0,remark)
                                    other.append(remark)
                                else:
                                    if remark in noderemark:
                                        continue
                                    else:
                                        Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                                        'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
                                        noderemark += remark
                                        Peoxies +='- '+str(Json)+'\n'
                                        groups[i].insert(0,remark)
                                        other.append(remark)                                
                        else :
                            continue
                    else :                         #每组是否有多个匹配要求   @香港&1倍@美国     适用 美国这组
                        if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '' and nodeR['protocol'] == 'origin' and nodeR['obfs'] == 'plain':    #判断是否为ssr
                            if nodeR['method'] == 'none':
                                continue
                            Json={ 'name': remark, 'type': 'ss', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                            'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'obfs': nodeR['obfs'] }
                            Peoxies +='- '+str(Json)+'\n'
                            groups[i].insert(0,remark)
                            other.append(remark)
                        else:
                            if remark in noderemark:
                                continue
                            else:
                                Json={ 'name': remark, 'type': 'ssr', 'server': nodeR['server'], 'port': nodeR['server_port'], 'password':nodeR['password'] , \
                                'cipher': nodeR['method'], 'protocol': nodeR['protocol'], 'protocolparam': nodeR['protocol_param'], 'obfs': nodeR['obfs'], 'obfsparam': nodeR['obfs_param'] }
                                noderemark += remark
                                Peoxies +='- '+str(Json)+'\n'
                                groups[i].insert(0,remark)
                                other.append(remark)
                else:                              #每组第一个不匹配
                    continue

        #print(groups)  
        clashgroup = '\n'
        clashname = ''
        for i in range(len(groups)):
            if i == 0:
                continue
            clashgroup  += '- { '+'name: "{name}故障切换", type: "fallback", "proxies": '.format(name=str(flags[i])) + str(groups[i]) + ', url: "http://www.gstatic.com/generate_204", interval: 450 }\n'
            clashname += '"{name}故障切换",'.format(name=str(flags[i]))
        clashname = clashname[:-1]
        #print(clashgroup)
        #print(clashname)

        proxy = str(other)
        proxy1 = proxy[1:-1]
        if selectfirst == 'yes':
            ProxyGroup='\n\nProxy Group:\n\n' + clashgroup + \
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "代理模式", type: select, proxies: [ "手动选择",'  + clashname +  ', "DIRECT",] }\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "Youtube", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "动画疯", type: select, proxies:  ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                    '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                    '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                    '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                    'Rule:\n'   
        else :
            ProxyGroup='\n\nProxy Group:\n\n' + clashgroup + \
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "代理模式", type: select, proxies: [ '  + clashname +  ',"手动选择","DIRECT"] }\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "Youtube", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "动画疯", type: select, proxies:  ["代理模式",'+proxy1+'] }\n'\
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

