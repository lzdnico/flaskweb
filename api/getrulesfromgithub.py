# coding=utf-8
import  sys
import  base64
import  re
import  requests
import  urllib3
import  urllib
import  json
import  time
import codecs
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
            i = i+1
            print('重新下载：'+url)

def getrules():             # 自定义规则
    
    try:
        rules = Retry_request('https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/Pro.yaml')        #请求规则_神机规则
       
        l_rule =  rules.split('Rule:\n')[1].replace('GlobalMedia','国际媒体').replace('HKMTMedia','国内媒体').replace('Hijacking','恶意网站').replace('Final','漏网之鱼').replace('PROXY','代理模式')
        l_rule2 =  rules.split('Rule:\n')[1].replace('GlobalMedia','🌍 国外媒体').replace('HKMTMedia','🌏 国内媒体').replace('Hijacking','⛔️ 恶意网站').replace('Final','🐟 漏网之鱼').replace('PROXY','🔰 代理模式')
 
        nf_rule = l_rule.split('# > Netflix\n')[1].split('# > niconico\n')[0].replace('国际媒体','Netflix') + '\n'
        nf_rule2 = l_rule.split('# > Netflix\n')[1].split('# > niconico\n')[0].replace('国际媒体','🎥 NETFLIX') + '\n'
        nf2_rule = l_rule.split('# > Netflix\n')[2].split('# GeoIP China\n')[0].replace('国际媒体','Netflix') + '\n'
        nf2_rule2 = l_rule.split('# > Netflix\n')[2].split('# GeoIP China\n')[0].replace('国际媒体','🎥 NETFLIX') + '\n'

        bahamut_rule = l_rule.split('# > Bahamut\n')[1].split('# > BBC iPlayer\n')[0].replace('国际媒体','动画疯') + '\n'
        bahamut_rule2 = l_rule.split('# > Bahamut\n')[1].split('# > BBC iPlayer\n')[0].replace('国际媒体','📺 巴哈姆特') + '\n'

        ytb_rule = l_rule.split('# > Youtube\n')[1].split('# > 愛奇藝台灣站\n')[0].replace('国际媒体','Youtube') + '\n'
        ytb_rule2 = l_rule.split('# > Youtube\n')[1].split('# > 愛奇藝台灣站\n')[0].replace('国际媒体','📹 YouTube') + '\n'
        
        apple ='# > Apple\n'+ l_rule.split('# > Apple\n')[2].split('# Local Area Network\n')[0].replace('Apple','Apple') + '\n'
        apple2 ='# > Apple\n'+ l_rule.split('# > Apple\n')[2].split('# Local Area Network\n')[0].replace('Apple','🍎 苹果服务') + '\n'

        with open("./config/selfrules.yml", "r",encoding = 'utf-8') as f:
            selfrule = '\n'+f.read() + '\n'

        last = l_rule.split('# GeoIP China')[1]
        last2 = l_rule2.split('# GeoIP China')[1]
        above = l_rule.split('# GeoIP China')[0]
        above2 = l_rule2.split('# GeoIP China')[0]
        l_rule =  apple + bahamut_rule + ytb_rule + nf_rule + nf2_rule + above + selfrule + last

        l_rule2 =  apple2 + bahamut_rule2 + ytb_rule2 + nf_rule2 + nf2_rule2 + above2 + selfrule + last2
        with codecs.open("./config/lrules.yml", "w",encoding = 'utf-8') as f:
            f.writelines(l_rule) 
        with codecs.open("./config/customlrules.yml", "w",encoding = 'utf-8') as f:
            f.writelines(l_rule2) 

 

    
    except Exception as e:
        print(e)

if __name__ == '__main__':
    getrules()