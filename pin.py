from ddk.api.rest.DdkGoodsDetail import DdkGoodsDetail
from ddk.api.rest.DdkGoodsPromotionUrlGenerate import DdkGoodsPromotionUrlGenerate
from ddk import appinfo
import re


class PDD():

    def __init__(self,client_id,client_secret,pid):
        self.client_id = client_id
        self.client_secret = client_secret
        self.pid = pid

    def get_id(self,url):
        r = re.compile(r'goods_id=\d+')
        id_list = r.findall(url)
        id = id_list[0].strip('goods_id=') if len(id_list)>0 else None
        return id

    def get_coupon(self,url):
        id = self.get_id(url)
        if id:
            req = DdkGoodsDetail()
            req.set_app_info(appinfo(appkey=self.client_id, secret=self.client_secret))
            req.goods_id_list = f'[{id}]'
            try:
                r = req.getResponse()
                if r['goods_detail_response']['goods_details'][0]['has_coupon']:
                    goods_price = float(r['goods_detail_response']['goods_details'][0]['min_group_price'])/100
                    coupon_price = float(r['goods_detail_response']['goods_details'][0]['coupon_discount'])/100
                    goods_price_after = goods_price-coupon_price
                    coupon_text = '【在售价】%s元，【券后价】%s元'%(goods_price,str(goods_price_after))
                    coupon_url = self.transformer(url)
                else:
                    coupon_text = '此商品无专属优惠券'
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
        if id:
            req = DdkGoodsPromotionUrlGenerate()
            req.set_app_info(appinfo(appkey=self.client_id, secret=self.client_secret))
            req.goods_id_list = f'[{id}]'
            req.generate_short_url = True
            req.p_id = self.pid
            req.multi_group = True
            try:
                r = req.getResponse()
                short_url = r['goods_promotion_url_generate_response']['goods_promotion_url_list'][0]['short_url']
            except:
                short_url = url
        else:
            short_url = url
        return short_url


if __name__ == '__main__':
    client_id = 'xxxxx'
    client_secret = 'xxxxx'
    pid = 'xxxxxxx'
    url = 'https://mobile.yangkeduo.com/goods2.html?goods_id=4435268166'
    couponer = PDD(client_id,client_secret,pid)
    coupon_text,coupon_url = couponer.get_coupon(url)
    print(coupon_text,coupon_url)

