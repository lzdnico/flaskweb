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
            #if "30倍" in remark:        #用于剔除高倍率节点
                #continue
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
            return api.aff.aff
