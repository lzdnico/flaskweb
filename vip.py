from mitmproxy import http
from mitmproxy import ctx
import json

#pip3 install mitmproxy
#mitmdump  用于生成证书
#将ca.pem 证书安装到手机上，信任
#screen -R mitm
#mitmdump -p 8080 --set block_global=false -s mitm.py

class modify:
    def response(self, flow):
        try:
            if flow.request.url.startswith("https://api.termius.com/api/v3/bulk/account/"):
                obj = json.loads(flow.response.get_text())
                obj["account"]['pro_mode'] = True
                obj['account']['plan_type'] = "Premium"
                obj['account']['user_type'] = "Premium"
                obj['account']['current_period']['until'] = "2099-10-10T03:27:34"
                flow.response.set_text(json.dumps(obj))
            
            if flow.request.url.startswith('http://vip1.kuwo.cn'):  
                #print(flow.request.url)              
                vip = '/vip/v2/user/vip'
                time = '/vip/spi/mservice'
                if vip in flow.request.url:
                    obj = json.loads(flow.response.get_text())
                    obj['data']["isNewUser"] = "2"
                    obj['data']["vipLuxuryExpire"] = "1835312949000"
                    obj['data']["time"] = "1961170340993"
                    obj['data']["isYearUser"] = "2"
                    obj['data']["vipmExpire"] = "1835312949000"
                    obj['data']["vipOverSeasExpire"] = "1835312949000"
                    obj['data']["vipExpire"] = "1835312949000"
                    obj['data']["vip3Expire"] = "1835312949000"
                    flow.response.set_text(json.dumps(obj))
                if time in flow.request.url:
                    obj = json.loads(flow.response.get_text())
                    obj["isVIPMAutoPay"] = 2
                    obj["isVIPLuxAutoPay"] = 2
                    flow.response.set_text(json.dumps(obj))

            if flow.request.url.startswith('https://vsco.co') :
                path = '/api/subscriptions/2.1/user-subscriptions/'
                if path in flow.request.url:
                    obj = json.loads(flow.response.get_text())
                    #print('before'+str(obj))
                    obj['user_subscription']["expires_on_sec"] = 1655536094
                    obj['user_subscription']["expired"] = False
                    obj['user_subscription']["payment_type"] = 2
                    obj['user_subscription']["is_trial_period"] = True
                    obj['user_subscription']["starts_on_sec"] = 1560831070
                    obj['user_subscription']["is_active"] = True
                    obj['user_subscription']["auto_renew"] = True
                    obj['user_subscription']["last_verified_sec"] = 1560831070
                    obj['user_subscription']["subscription_code"] = "VSCOANNUAL"
                    obj['user_subscription']["user_id"] = 54624336
                    obj['user_subscription']["source"] = 1
                    #print(json.dumps(obj))
                    flow.response.set_text(json.dumps(obj))                    

            if flow.request.url.startswith('https://api.calm.com'):
                obj = json.loads(flow.response.get_text())
                #print(obj)
                obj["subscription"]= {
                    "in_free_trial_window": True,
                    "subscription_plan": "com.calm.yearly.trial.one_week.usd_50",
                    "began": "2019-04-22T12:12:54.000Z",
                    "is_lifetime": True,
                    "valid": True,
                    "is_renewable": True,
                    "is_in_billing_retry_period": False,
                    "will_renew": True,
                    "expires": "2099-04-29T12:12:54.000Z",
                    "user_id": "KgagpU1URv",
                    "type": "ios",
                    "is_canceled": False,
                    "free_trial_began": "2019-04-22T12:12:54.000Z",
                    "coupon_used": False,
                    "has_ever_done_free_trial": True,
                    "is_free": False,
                    "ios_details": {
                        "product_id": "com.calm.yearly.trial.one_week.usd_50",
                        "began": "2019-04-22T12:12:54.000Z",
                        "is_free_trial": True,
                        "id": "540000370675471",
                        "is_canceled": False,
                        "is_renewable": True,
                        "free_trial_ended": "2099-04-29T12:12:54.000Z",
                        "free_trial_began": "2019-04-22T12:12:54.000Z",
                        "will_renew": True,
                        "original_transaction_id": "540000370675471",
                        "expires": "2099-04-29T12:12:54.000Z"
                        },
                    "free_trial_ended": "2099-04-29T12:12:54.000Z"
                    }
                flow.response.set_text(json.dumps(obj))
        
            if flow.request.url.startswith('https://api.gotokeep.com'):  
                #print(flow.request.url)              
                vip1 = 'dynamic'
                vip2 = 'subject'
                if vip1 in flow.request.url:
                    obj = json.loads(flow.response.get_text())
                    #print(obj)
                    obj['data']['permission']['isMembership'] = True
                    obj['data']['permission']['membership'] = True
                    obj['data']['permission']['inSuit'] = True
                    flow.response.set_text(json.dumps(obj))
                if vip2 in flow.request.url:
                    obj = json.loads(flow.response.get_text())
                    #print(flow.request.url)
                    for i in range(len(obj['data']['subjectInfos'])) :
                        obj['data']['subjectInfos'][i]['needPay'] = False                          
                        #print('keep')  
                    #print(obj['data']['subjectInfos'])            
                    flow.response.set_text(json.dumps(obj))
        except Exception as e:
            print(e)

addons = [
    modify()
]