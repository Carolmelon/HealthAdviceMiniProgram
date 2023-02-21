from app1.models import Article_category1, Product_categories
from bs4 import BeautifulSoup
import random
import hashlib
from decimal import Decimal
from TimeProject.settings import app_id, app_secret,Mch_id,Mch_key

# 文章
# 展开前端传回的嵌套数组,返回id(unique),深度优先遍历
def expand(ArticleClassesData):
    def inner_expand(list_node, ids):
        # print(list_node, "\n=====\n")
        if not list_node['children']:
            return
        for child_list_node in list_node['children']:
            if child_list_node.get('level'):  # 说明是共有的分类
                ids.append(child_list_node['id'])
            inner_expand(child_list_node, ids)
    ids = []
    for level_1_list_node in ArticleClassesData:
        if level_1_list_node.get('level'):  # 说明是共有的分类
           ids.append(level_1_list_node['id'])
        inner_expand(level_1_list_node, ids)
    return ids

def list_to_model(list_node, current_node):
    #child_list_node 当前前端返回的项
    #current_child_node 数据库对应的子节点
    all_children_list_node = list_node['children']
    if not all_children_list_node:
        return
    for child_list_node in all_children_list_node:
        current_child_node = None
        if not child_list_node.get('level'):  # 说明是才添加的新分类
            current_child_node = Article_category1.objects.create(
                name=child_list_node['label'],
            )
        else:
            current_child_node = Article_category1.objects.get(id=int(child_list_node['id']))
            if current_child_node.name != child_list_node['label']:
                current_child_node.name = child_list_node['label']
                current_child_node.save()
        current_child_node.level = current_node.level + 1
        current_child_node.father = current_node
        current_child_node.save()
        list_to_model(child_list_node, current_child_node)

def product_cat_list_to_model(list_node, current_node):
    #child_list_node 当前前端返回的项
    #current_child_node 数据库对应的子节点
    all_children_list_node = list_node['children']
    if not all_children_list_node:
        return
    for child_list_node in all_children_list_node:
        current_child_node = None
        if not child_list_node.get('level'):  # 说明是才添加的新分类
            current_child_node = Product_categories.objects.create(
                name=child_list_node['label'],
            )
        else:
            current_child_node = Product_categories.objects.get(id=int(child_list_node['id']))
            if current_child_node.name != child_list_node['label']:
                current_child_node.name = child_list_node['label']
                current_child_node.save()
        current_child_node.level = current_node.level + 1
        current_child_node.father = current_node
        current_child_node.save()
        product_cat_list_to_model(child_list_node, current_child_node)

def htmlToWxml(s):
    s = s.replace("<p","<view")
    s = s.replace("</p>","</view>")
    s = s.replace("span","text")
    s = s.replace("<strong>","<text style=\"font-weight:bold\">")
    s = s.replace("</strong>","</text>")
    return s


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象

    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """

    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}

    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据

    :param data: dict 对象
    :return: xml 格式数据
    """

    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))

#生成随机字符串
def getNonceStr():
    '''
    :return: 长度为30的随机字符串
    '''

    data="123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
    nonce_str  = ''.join(random.sample(data , 30))
    return nonce_str

# 生成签名的函数
def paysign(body, nonce_str, notify_url, openid, out_trade_no, spbill_create_ip, total_fee):
    ret = {
        "appid": app_id,
        "body": body,
        "mch_id": Mch_id,
        "nonce_str": nonce_str,
        "notify_url": notify_url,
        "openid": openid,
        "out_trade_no": out_trade_no,
        "spbill_create_ip": spbill_create_ip,
        "total_fee": total_fee,
        "trade_type": 'JSAPI'
    }
    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, Mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()

# 生成商品订单号，方式一：
def getWxPayOrdrID():
    import datetime

    date = datetime.datetime.now()
    # 根据当前系统时间来生成商品订单号。时间精确到微秒
    payOrdrID = date.strftime("%Y%m%d%H%M%S%f")
    return payOrdrID

#获取全部参数信息，封装成xml,传递过来的openid和客户端ip，和价格需要我们自己获取传递进来
def get_bodyData(openid, client_ip, price, body, notify_url, out_trade_no):
    '''
    :param openid: 用户标识
    :param client_ip: 用户ip
    :param price: 商品价格
    :param body: 商品名：卓越壹生-***
    :param notify_url: 填写支付成功的回调地址，微信确认支付成功会访问这个接口
    :param out_trade_no: 商家订单号
    :return:
    '''

    nonce_str = getNonceStr()  # 随机字符串
    total_fee = str(price)  # 订单价格，单位是 分
    # 获取签名
    sign = paysign(body, nonce_str, notify_url, openid, out_trade_no, client_ip, total_fee)

    bodyData = '<xml>'
    bodyData += '<appid>' + app_id + '</appid>'  # 小程序ID
    bodyData += '<body>' + body + '</body>'  # 商品描述
    bodyData += '<mch_id>' + Mch_id + '</mch_id>'  # 商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    bodyData += '<notify_url>' + notify_url + '</notify_url>'  # 支付成功的回调地址
    bodyData += '<openid>' + openid + '</openid>'  # 用户标识
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    bodyData += '<spbill_create_ip>' + client_ip + '</spbill_create_ip>'  # 客户端终端IP
    bodyData += '<total_fee>' + total_fee + '</total_fee>'  # 总金额 单位为分
    bodyData += '<trade_type>JSAPI</trade_type>'  # 交易类型 小程序取值如下：JSAPI
    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'

    return bodyData

#获取返回给小程序的paySign
def get_paysign(prepay_id,timeStamp,nonceStr):
    pay_data={
                'appId': app_id,
                'nonceStr': nonceStr,
                'package': "prepay_id="+prepay_id,
                'signType': 'MD5',
                'timeStamp':timeStamp
    }
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, Mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()

def priceToInt(price):
    '''

    :param price: str类型的price，形式不限(如:5.1, 0, 2.33)，单位：元
    :return: price: str类型，整数，单位：分
    '''
    standard_price = str(Decimal(price).quantize(Decimal("0.00")))
    int_price = str(int("".join(standard_price.split("."))))
    return int_price

def intToPrice(price):
    '''

    :param price:单位分,形式是整数
    :return:单位元,形式是0.00
    '''
    d = Decimal(price) / Decimal("100")
    d = str(d.quantize(Decimal("0.00")))
    return d