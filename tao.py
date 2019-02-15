from top.api import TbkDgMaterialOptionalRequest,TbkTpwdCreateRequest
from top import appinfo
import requests



from bs4 import BeautifulSoup
import re


class Couponer():

    def __init__(self,appkey,appsecret,mm,adzoneid):
        self.appkey = appkey
        self.appsecret = appsecret
        self.mm = mm
        self.adzoneid = adzoneid

    def get_info(self,share_text):
        title_re = re.compile(r'【.*】')
        url_re = re.compile(r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        title_list = title_re.findall(share_text)
        url_list = url_re.findall(share_text)
        if len(title_list)>0 and len(url_list)>0:
            title = title_list[0].strip('【').strip('】')
            tb_url = url_list[0]
            return {'title':title,'tb_url':tb_url}
        else:
            return None

    def get_id(self,tb_url):
        resp = requests.get(tb_url).text
        bsj = BeautifulSoup(resp, 'lxml')
        script_with_url = bsj.find_all('script')[1]
        r = re.compile(r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        murl = r.findall(str(script_with_url))[0]
        ok_url = requests.get(murl).url
        start = ok_url.find('id')
        end = ok_url.find('&',start)
        id = int(ok_url[start + 3:end].strip())
        return id

    def get_tkl(self,share_text):
        info = self.get_info(share_text)
        if info:
            title = info['title']
            url = info['tb_url']
            id = self.get_id(url)
            req1 = TbkDgMaterialOptionalRequest()
            req1.set_app_info(appinfo(appkey, appsecret))
            req1.adzone_id = self.adzoneid
            req1.q = title
            resp1 = req1.getResponse()
            result = [i for i in resp1['tbk_dg_material_optional_response']['result_list']['map_data'] if
                      int(i['num_iid']) == id][0]
            if len(result['coupon_info'])<1:
                taobao_message = '商品无优惠券'
            else:
                price0 = result['zk_final_price']
                coupon_url = 'https:' + result['coupon_share_url']
                coupon_info = result['coupon_info']
                coupon_start = coupon_info.find('减')
                coupon_price = coupon_info[coupon_start:].strip('减').strip('元')
                img_url = result['pict_url']
                req2 = TbkTpwdCreateRequest()
                req2.set_app_info(appinfo(appkey, appsecret))
                req2.text = title
                req2.url = coupon_url
                req2.logo = img_url
                resp2 = req2.getResponse()
                tkl = resp2['tbk_tpwd_create_response']['data']['model']
                taobao_message = '%s\n【在售价】%s元\n【券后价】%s元\n复制这条信息，打开「手机绹宝」领券下单%s'%(title,price0,
                                                                                  str(int(price0)-int(coupon_price)),tkl)
            return taobao_message




if __name__ == '__main__':
    appkey = '25520322'
    appsecret = '99fe36c2bf904fcabff8c275588cf662'
    mm = 'mm_46597913_21620290_85978550206'
    adzoneid = '85978550206'
    couponer = Couponer(appkey=appkey,appsecret=appsecret,mm=mm,adzoneid=adzoneid)
    share_text = '【鸿星尔克运动鞋女休闲鞋新款复古粉色老爹鞋防滑耐磨轻便跑鞋女鞋】https://m.tb.cn/h.3FTt7wD?sm=2b5b6a 点击链接，再选择浏览器咑閞；或復·制这段描述￥IbnQbtte3eU￥后到淘♂寳♀'
    taobao_message = couponer.get_tkl(share_text)
    print(taobao_message)


