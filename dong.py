import requests
import re


class JD():

    def __init__(self,apikey):
        self.apikey = apikey

    def get_id(self,url):
        r = re.compile(r'\d+')
        id_list = r.findall(url)
        id = int(id_list[0]) if len(id_list)>0 else None
        return id

    def get_coupon(self,url):
        api = 'http://api-gw.haojingke.com/index.php/api/index/myapi?type=goodsdetail'
        id = self.get_id(url)
        if id:
            data = {
                'apikey': self.apikey,
                'skuid': id,
                'source_type': 1
            }
            try:
                r = requests.post(api, data=data)
                j = r.json()
                if j['data'] == '' or j['data']['couponList'] == '':
                    coupon_text = '此商品无专属优惠券'
                    coupon_url = self.transformer(url)
                else:
                    good_price = j['data']['wlPrice']
                    good_price_after = j['data']['wlPrice_after']
                    coupon_text = '【在售价】%s元，【券后价】%s元'%(good_price,good_price_after)
                    coupon_url = self.transformer(url)
            except:
                coupon_text = '此商品无专属优惠券'
                coupon_url = self.transformer(url)
        else:
            coupon_text = '此商品无专属优惠券'
            coupon_url = self.transformer(url)
        return coupon_text,coupon_url

    def transformer(self,url):
        id = self.get_id(url)
        api = 'http://api-gw.haojingke.com/index.php/api/platform/openapi?type=unionurl'
        if id:
            data = {
                'apikey': self.apikey,
                'skuid': id,
                'source_type': 1,
                'pid':1
            }
            try:
                r = requests.post(api,data)
                j = r.json()
                ok_url = j['data'] if j['data'] != '' else url
            except:
                ok_url = url
        else:
            ok_url = url
        return ok_url


if __name__ == '__main__':
    apikey = 'xxxxxx'
    url = 'http://item.jd.com/32524101190.html'
    couponer = JD(apikey)
    coupon_text,coupon_url = couponer.get_coupon(url)
    print(coupon_text,coupon_url)




