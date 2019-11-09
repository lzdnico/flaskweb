# coding=utf-8
import  sys
import  base64
import  re
import  requests
import  urllib3
import  urllib
import  json
import  time
import  api.aff
urllib3.disable_warnings()

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
        obfs_param = safe_base64_decode(re.search(r'obfsparam=([^&]+)',pass_param_spilted[1]).group(1))
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
            if nodeR['protocol_param'] == '' and  nodeR['obfs_param'] == '' and nodeR['protocol'] == 'origin' and nodeR['obfs'] == 'plain':    #判断是否为ssr
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
                    '- { name: "代理模式", type: select, proxies: ["手动选择","故障切换","DIRECT"] }\n'\
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "Youtube", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "动画疯", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国际媒体", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式","手动选择"] }\n'\
                    '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                    '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                    '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT"] }\n\n\n'\
                    'Rule:\n'
        else :
            ProxyGroup='\n\nProxy Group:\n\n'\
                    '- { name: "代理模式", type: select, proxies: [ "故障切换","手动选择","DIRECT"] }\n'\
                    '- { name: "故障切换", type: "fallback", "proxies": ' + proxy + ', url: "http://www.gstatic.com/generate_204", interval: 450'+ '}\n'\
                    '- { name: "手动选择", type: "select", "proxies": ' + proxy + '}\n'\
                    '- { name: "Netflix", type: select, proxies: '+proxy+' }\n'\
                    '- { name: "Youtube", type: select, proxies: ["代理模式",'+proxy1+'] }\n'\
                    '- { name: "动画疯", type: select, proxies:  ["代理模式",'+proxy1+'] }\n'\
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
            return api.aff.aff
