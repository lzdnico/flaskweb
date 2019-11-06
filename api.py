# coding=utf-8
import sys
import flask_restful
import  base64
import  re
import  requests
import urllib3
import urllib
import urllib.parse
import json
import time
import codecs
import api.qx
import api.loon
import api.group
import api.customclash
import api.customssr
import api.clash
import api.aff
import api.groupload
import api.groupchoose
from flask import Flask,render_template,request
urllib3.disable_warnings()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    with codecs.open("./config/ip", "a",encoding = 'utf-8') as f:
        f.writelines(ip+'\n')
    if request.method == "POST":
        sub = request.form['left']
        with codecs.open("./config/ip", "a",encoding = 'utf-8') as f:
            f.writelines(sub+'\n')
        custom = urllib.parse.quote(request.form['custom'])
        custommethod = urllib.parse.quote(request.form['custommethod'])
        Clash = 'http://{ip}/clashr/nico?sublink='.format(ip=api.aff.apiip)+str(sub)+'&selectfirst=no'
        if custom == '':
            CustomClash = '假设想要香港就@香港，假设想要香港的2倍节点就@香港&2倍。支持多个@即：@PCCW@CMHK@香港&2倍'
            CustomGroupClash = '同上'
            CustomSSR =   '请填入想要的节点，同上'
        else:
            CustomClash = 'http://{ip}/clashr/nico?sublink={sub}&custom={custom}&selectfirst=no'.format(ip=api.aff.apiip,sub=str(sub),custom=str(custom))
            if custommethod == '':
                CustomGroupClash = '请在《填入节点模式》中按照说明填写'
            else:
                CustomGroupClash = 'http://{ip}/clashr/customgroup?sublink={sub}&custom={custom}&custommethod={custommethod}&selectfirst=no'.format(ip=api.aff.apiip,sub=str(sub),custom=str(custom),custommethod=str(custommethod))
            CustomSSR = 'http://{ip}/ssr/nico?sublink={sub}&custom={custom}'.format(ip=api.aff.apiip,sub=str(sub),custom=str(custom))
        QX = 'http://{ip}/qx/nico?sublink={sub}&tag=stc'.format(ip=api.aff.apiip,sub=str(sub))
        Loon = 'http://{ip}/loon/nico?sublink={sub}&tag=stc'.format(ip=api.aff.apiip,sub=str(sub))
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人打开了你的托管页面 : \n')+sub+'\n调用IP为：'+ip+'\n参数为'+custom)
        return render_template('index.html', Clash = Clash,QX = QX,Loon=Loon,CustomClash = CustomClash,CustomSSR = CustomSSR,Custom =request.form['custom'] ,sub = sub,CustomGroupClash=CustomGroupClash,Custommethod=request.form['custommethod'])
    return render_template('index.html')

@app.route('/clashr/nico', methods=['GET', 'POST'])
def clashapi():
    try:
        ip = request.remote_addr
        sub = request.args.get('sublink')
        #print(sub)
        try:
            arg = request.args.get('selectfirst')
        except Exception as e:
            arg = 'no'
        #print(arg)
        try:
            custom = request.args.get('custom')
        except Exception as e:
            custom = ''
        #print(custom)
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了New_ClashAPI : \n'+sub))
        if custom == '' or custom == None :
            return api.clash.writeRules(sub,arg)
        else :
            return  api.customclash.writeRulescustom(sub,custom,arg)
    except Exception as e:
        return '检测调用格式是否正确'+ api.aff.aff

@app.route('/clashr/customgroup', methods=['GET', 'POST'])
def clashapigroup():
    try:
        ip = request.remote_addr
        sub = request.args.get('sublink')
        #print(sub)
        try:
            arg = request.args.get('selectfirst')
        except Exception as e:
            arg = 'no'
        #print(arg)
        try:
            custom = request.args.get('custom')
        except Exception as e:
            custom = ''
        try:
            custommethod = request.args.get('custommethod')
        except Exception as e:
            custom = ''
        #print(custom)
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了New_Clash分组API : \n'+sub+str(custom)))
        if custom == '' or custom == None :
            return api.clash.writeRules(sub,arg)
        else :
            return  api.groupchoose.writeRulescustom(sub,custom,custommethod,arg)
    except Exception as e:
        return '检测调用格式是否正确'+ api.aff.aff

@app.route('/qx/nico', methods=['GET', 'POST'])
def qxapi():
    try:
        ip = request.remote_addr
        sub = request.args.get('sublink')            
        #print(sub)
        tag=request.args.get('tag')
        #print(tag)
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了New_QXAPI : \n'+sub+'\n参数为'+tag))
        return  api.qx.getqxrules(sub,tag)

    except Exception as e:
        return '请确认调用格式适合正确'+ api.aff.aff

@app.route('/ssr/nico', methods=['GET', 'POST'])
def ssrapi():
    try:
        ip = request.remote_addr
        sub = request.args.get('sublink')             
        #print(sub)
        custom=request.args.get('custom')
        #print(tag)
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了New_SSRAPI : \n'+sub+'\n参数为'+custom))
        return  api.customssr.getcustomssrlink(sub,custom)

    except Exception as e:
        return '检测调用格式是否正确'+ api.aff.aff

@app.route('/loon/nico', methods=['GET', 'POST'])
def loonapi():
    try:
        ip = request.remote_addr
        sub = request.args.get('sublink').replace('!','&')              
        #print(sub)
        tag=request.args.get('tag')
        #print(tag)
        #requests.post('https://api.telegram.org/bot976092923:AAFqWi5Z6XqDffkdxDc7gqyDDMg12ufXFW8/sendMessage?chat_id=447216258&text={text}'.format(text='有人调用了New_LoonAPI : \n'+sub+'\n参数为'+tag))
        return  api.loon.getrules(sub,tag)
    except Exception as e:
        return '请确认调用格式适合正确'+ api.aff.aff

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=10010)            #自定义端口