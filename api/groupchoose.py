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

def getrules(emoji):             # 自定义规则
    
    try:
        finalrules=[]
        
        with open("./config/general.yml", "r",encoding = 'utf-8') as f:
            p_rule = f.read() + '\n'

        if emoji == 'yes':
            with open("./config/customlrules.yml", "r",encoding = 'utf-8') as f:
                l_rule = f.read()       
        else :
            with open("./config/lrules.yml", "r",encoding = 'utf-8') as f:
                l_rule = f.read()                
        
        Peoxies = 'Proxy:\n'
        finalrules.append(p_rule)
        finalrules.append(Peoxies)
        finalrules.append(l_rule)
        return finalrules
    except Exception as e:
        print(e)

def writeRulescustom(sublink,flagname,methods,emoji):    #客制化策略组及规则
    try:
        #print(sublink + 'custom')
        other=[]       
        Peoxies = ''
        noderemark = ''      #用于剔除节点标准
        data = Retry_request(sublink)    #请求订阅        
        ssrdata=safe_base64_decode(data).strip().split('\n')  
        flags = flagname.split('@')
        for i in range(len(flags)):
            while 1:
                if '港' in flags[i]:
                    flags[i] = '🇭🇰&' + flags[i]
                    break
                if '台' in flags[i] or '湾' in flags[i] or "彰化" in flags[i]  or "新北" in flags[i]:
                    flags[i] = '🇹🇼&' + flags[i]
                    break
                if "美" in flags[i]  or "圣克拉拉" in flags[i]  or "波特兰" in flags[i]  or "洛杉矶" in flags[i]  or "费利蒙" in flags[i]  or "圣何塞" in flags[i] or "达拉斯" in flags[i] or "芝加哥" in flags[i] or "凤凰城" in flags[i] or "西雅图" in flags[i] or "硅谷" in flags[i]:
                    flags[i] = '🇺🇸&' + flags[i]
                    break
                if "日" in flags[i]  or "埼玉" in flags[i]   or "东京" in flags[i] or "大阪" in flags[i]:
                    flags[i] = '🇯🇵&' + flags[i]
                    break
                if  '新' in flags[i] or '狮城' in flags[i]:
                    flags[i] = '🇸🇬&' + flags[i] 
                    break 
                if  '韩' in flags[i] or '首尔' in flags[i]:
                    flags[i] = '🇰🇷&' + flags[i]  
                    break
                if "俄罗斯"  in flags[i] or "圣彼得堡" in flags[i] :
                    flags[i] = '🇷🇺&' + flags[i]
                    break
                if "泰"  in flags[i] or "曼谷" in flags[i] :
                    flags[i] = '🇹🇭&' + flags[i]
                    break
                if "法兰克福"  in flags[i] or "德" in flags[i] :
                    flags[i] = '🇩🇪&' + flags[i]
                    break
                if "伦敦"  in flags[i] or "英" in flags[i] :
                    flags[i] = '🇬🇧&' + flags[i]
                    break
                if "悉尼" in flags[i]  or "澳大利亚" in flags[i] :
                    flags[i] = '🇦🇺&' + flags[i]
                    break
                else :
                    flags[i] = '&' + flags[i]
                    break            
        #ssrdata = data.strip().replace('==','').split('\n')     
        groups = [[] for _ in range(len(flags))]
        #print(groups)

        for i in range(len(ssrdata)):          #遍历节点                                         #节点组            
            ssrlink = safe_base64_decode(ssrdata[i].replace('ssr://','').replace('\r',''))
            nodeR = getnodeR(ssrlink)
            remark = nodeR['remark']  
            ##加图标
            while 1:
                if '港' in remark:
                    remark = '🇭🇰' + remark
                    break
                if '台' in remark or '湾' in remark or "彰化" in remark  or "新北" in remark:
                    remark = '🇹🇼' + remark
                    break
                if "美" in remark  or "圣克拉拉" in remark  or "波特兰" in remark  or "洛杉矶" in remark  or "费利蒙" in remark  or "圣何塞" in remark or "达拉斯" in remark or "芝加哥" in remark or "凤凰城" in remark or "西雅图" in remark or "硅谷" in remark:
                    remark = '🇺🇸' + remark
                    break
                if "日" in remark  or "埼玉" in remark   or "东京" in remark or "大阪" in remark:
                    remark = '🇯🇵' + remark
                    break
                if  '新' in remark or '狮城' in remark:
                    remark = '🇸🇬' + remark 
                    break 
                if  '韩' in remark or '首尔' in remark:
                    remark = '🇰🇷' + remark  
                    break
                if "俄罗斯"  in remark or "圣彼得堡" in remark :
                    remark = '🇷🇺' + remark
                    break
                if "泰"  in remark or "曼谷" in remark :
                    remark = '🇹🇭' + remark
                    break
                if "法兰克福"  in remark or "德" in remark :
                    remark = '🇩🇪' + remark
                    break
                if "伦敦"  in remark or "英" in remark :
                    remark = '🇬🇧' + remark
                    break
                if "悉尼" in remark  or "澳大利亚" in remark :
                    remark = '🇦🇺' + remark
                    break
                else :
                    break                                                           

            for i in range(len(flags)):     #遍历分组匹配规则
                if flags[i] == '':
                    continue                                
                if flags[i].split('&')[1] in remark:   #每组第一个匹配             
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
                                    groups[i].insert(0,remark)
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
                                groups[i].insert(0,remark)
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
        methods = methods.split('@')
        for i in range(len(groups)):
            if i == 0:
                continue
            if methods[i] == 'select' :
                clashgroup  += '- { ' + 'name: "{name}手动选择", type: "select", "proxies": '.format(name=str(flags[i]).replace('&','')) + str(groups[i]) + ', url: "http://www.gstatic.com/generate_204", interval: 450 }\n'
                clashname += '"{name}手动选择",'.format(name=str(flags[i]).replace('&',''))
            if methods[i] == 'fallback' :
                clashgroup  += '- { ' + 'name: "{name}故障切换", type: "fallback", "proxies": '.format(name=str(flags[i]).replace('&','')) + str(groups[i]) + ', url: "http://www.gstatic.com/generate_204", interval: 450 }\n'
                clashname += '"{name}故障切换",'.format(name=str(flags[i]).replace('&',''))
            if methods[i] == 'load-balance' :
                clashgroup  += '- { ' + 'name: "{name}负载均衡", type: "load-balance", "proxies": '.format(name=str(flags[i]).replace('&','')) + str(groups[i]) + ', url: "http://www.gstatic.com/generate_204", interval: 450 }\n'
                clashname += '"{name}负载均衡",'.format(name=str(flags[i]).replace('&',''))   
            if methods[i] == 'url-test' :
                clashgroup  += '- { ' + 'name: "{name}延迟最低", type: "url-test", "proxies": '.format(name=str(flags[i]).replace('&','')) + str(groups[i]) + ', url: "http://www.gstatic.com/generate_204", interval: 450 }\n'
                clashname += '"{name}延迟最低",'.format(name=str(flags[i]).replace('&',''))                 
        clashname = clashname[:-1]
        #print(clashgroup)
        #print(clashname) 
        proxy = str(other)
        proxy1 = proxy[1:-1]

        rules = getrules(emoji)
        if emoji == 'yes':
            ProxyGroup='\n\nProxy Group:\n\n' \
                        '- { name: "🔰 代理模式", type: select, proxies: ['  + clashname + ', "DIRECT",] }\n'\
                        '- { name: "🎥 NETFLIX", type: select, proxies: ["🔰 代理模式",'+ clashname +'] }\n'\
                        '- { name: "📹 YouTube", type: select, proxies: ["🔰 代理模式",'+ clashname +'] }\n'\
                        '- { name: "📺 巴哈姆特", type: select, proxies: ["🔰 代理模式",'+ clashname +'] }\n'\
                        '- { name: "🌍 国外媒体", type: select, proxies: ["🔰 代理模式",'+ clashname +'] }\n'\
                        '- { name: "🌏 国内媒体", type: select, proxies: ["DIRECT","🔰 代理模式",'+ clashname +'] }\n'\
                        '- { name: "⛔️ 恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                        '- { name: "🍎 苹果服务", type: select, proxies: ["DIRECT", "🔰 代理模式"] }\n'\
                        '- { name: "🐟 漏网之鱼", type: select, proxies: ["🔰 代理模式", "DIRECT",'+clashname+'] }'+ clashgroup +'\n'\
                        'Rule:\n'
        else :
            ProxyGroup='\n\nProxy Group:\n\n' \
                        '- { name: "代理模式", type: select, proxies: ['  + clashname + ', "DIRECT",] }\n'\
                        '- { name: "Netflix", type: select, proxies: ["代理模式",'+ clashname +'] }\n'\
                        '- { name: "Youtube", type: select, proxies: ["代理模式",'+ clashname +'] }\n'\
                        '- { name: "动画疯", type: select, proxies: ["代理模式",'+ clashname +'] }\n'\
                        '- { name: "国际媒体", type: select, proxies: ["代理模式",'+ clashname +'] }\n'\
                        '- { name: "国内媒体", type: select, proxies: ["DIRECT","代理模式",'+ clashname +'] }\n'\
                        '- { name: "恶意网站", type: select, proxies: ["REJECT", "DIRECT"] }\n'\
                        '- { name: "Apple", type: select, proxies: ["DIRECT", "代理模式"] }\n'\
                        '- { name: "漏网之鱼", type: select, proxies: ["代理模式", "DIRECT",'+clashname+'] }'+ clashgroup +'\n'\
                        'Rule:\n'               
                    
        currenttime = '# 更新时间为（看分钟就行，不知道哪个时区）：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        content = currenttime+rules[0]+rules[1]+Peoxies+ProxyGroup+rules[2]
        return content

    except Exception as e:
            return api.aff.aff

