# -*- coding: utf-8 -*-
import requests
import json
import re
from promotion import ServicePromotionGetcodeRequest

class Changer():
    def __init__(self,appkey,appsecret,apptoken,unionId,webID,baidutoken):
        self.appkey = appkey
        self.appsecret = appsecret
        self.apptoken = apptoken
        self.baidutoken = baidutoken
        self.webid = webID
        self.unionid = unionId

    def dwz(self,url):
        host = 'https://dwz.cn'
        path = '/admin/v2/create'
        api_url = host+path
        content_type = 'application/json'
        bodys = {'url':str(url)}
        headers = {'Content-Type':content_type, 'Token':self.baidutoken}
        response = requests.post(api_url,data = json.dumps(bodys),headers = headers)
        short_url = response.json()['ShortUrl']
        return short_url

    def get_reurl(self,re_object):
        url = re_object.group(0)
        return self.change(url)

    def change(self,url):
        promotion = ServicePromotionGetcodeRequest(self.appkey,self.appsecret)
        promotion.promotionType = 7
        promotion.unionId = self.unionid
        promotion.channel = 'WL'
        promotion.webId = self.webid
        promotion.adttype = '6'

        if 'u.jd.com' in url:
            url2 = self.jf_url(url)
            if 'plogin' not in url2:
                url = url2
        if url.isnumeric():
            url = 'https://item.jd.com/'+str(url)
        promotion.materialId = url
        r = promotion.getResponse(self.apptoken)
        try:
            promotion_url = eval(r['jingdong_service_promotion_getcode_responce']['queryjs_result'])['url']
        except:
            promotion_url = url

        short_url = self.dwz(promotion_url)
        return short_url


    def sub_url(self,content):
        r = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        re_content = re.sub(r,self.get_reurl,content)
        return re_content

    def jf_url(self,url):
        r = requests.get(url)
        b = r.text.find('hrl')
        e = r.text.find(';',b)
        hrl = r.text[b+5:e-1]
        ok_url = requests.get(hrl).url
        return ok_url




