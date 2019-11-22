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
from flask import Flask,render_template,request
urllib3.disable_warnings()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST": 

        tool=request.values.get('tool')
        sub = request.form['left']
        #pg = urllib.parse.quote(request.form['custom'])
        #pg = request.form['custom']
        rules = request.form.getlist('snippet')
        customrule = '&rules='
        for rule in rules:
            customrule += str(rule)+'+'
        print(customrule)
        return render_template('tfirst.html', api = 'https://gfwsb.114514.best/'+tool+'?'+'url='+urllib.parse.quote(sub),sub=sub)
    return render_template('tfirst.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=10086)            #自定义端口