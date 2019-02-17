import requests
import re


class JD():

    def __init__(self,apikey):
        self.apikey = apikey

    def get_id(self,url):
        r = re.compile(r'\d+')
        id = int(r.findall(url)[0])
        return id

    def get_coupon(self,url):
        api = 'http://api-gw.haojingke.com/index.php/api/index/myapi?type=goodsdetail'
        id = self.get_id(url)
        data = {
            'apikey': self.apikey,
            'skuid': id,
            'source_type': 1
        }
        r = requests.post(api, data=data)
        j = r.json()
        if j['data'] == '' or j['data']['couponList'] == '':
            coupon_text = '此商品无专属优惠券'
            coupon_url = self.transformer(id)
            if coupon_url is None:
                coupon_url = url
        else:
            good_price = j['data']['wlPrice']
            good_price_after = j['data']['wlPrice_after']
            coupon_text = '【在售价】%s元，【券后价】%s元'%(good_price,good_price_after)
            coupon_url = self.transformer(id)
        return coupon_text,coupon_url

    def transformer(self,id):
        api = 'http://api-gw.haojingke.com/index.php/api/platform/openapi?type=unionurl'
        data = {
            'apikey': self.apikey,
            'skuid': id,
            'source_type': 1,
            'pid':1
        }
        r = requests.post(api,data)
        j = r.json()
        if j['data'] == '':
            return None
        else:
            ok_url = j['data']
            return ok_url


if __name__ == '__main__':
    apikey = 'xxxxxxx'
    url = 'https://item.m.jd.com/product/33307486713.html?dl_abtest=o&utm_source=iosapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&ad_od=share&ShareTm=tLcZWBxxNvq9DhkQF6BQKDBNNFeTlm7LpLgRz%2BxudNet/BJqNVYuPtFz9G%2BCAY7C1NMfynr3XtkXoLmzawpvfJsC8ozrcCS9s9moJii77BGm148WFZv5j0wrCUk9i9vZW4eef2h0ulzongP%2Bxcp7tr36Ppwh3XS9DpghXu/Tp9w='
    couponer = JD(apikey)
    coupon_text,coupon_url = couponer.get_coupon(url)
    print(coupon_text,coupon_url)




