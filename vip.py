from mitmproxy import http
from mitmproxy import ctx
import json

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
                obj = json.loads(flow.response.get_text())
                vip = '/vip/v2/user/vip'
                time = '/vip/spi/mservice'
                if vip in flow.request.url:
                    obj['data']["isNewUser"] = "2"
                    obj['data']["vipLuxuryExpire"] = "1835312949000"
                    obj['data']["time"] = "1961170340993"
                    obj['data']["isYearUser"] = "2"
                    obj['data']["vipmExpire"] = "1835312949000"
                    obj['data']["vipOverSeasExpire"] = "1835312949000"
                    obj['data']["vipExpire"] = "1835312949000"
                    obj['data']["vip3Expire"] = "1835312949000"
                if time in flow.request.url:
                    obj["isVIPMAutoPay"] = 2
                    obj["isVIPLuxAutoPay"] = 2
                flow.response.set_text(json.dumps(obj))
            

            if flow.request.url.startswith('http://api.calm.com'):
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
        except:
            print('erro')


    def request(self, flow):
        ctx.log.info('Modify request from'+ flow.request.url)
addons = [
    modify()
]