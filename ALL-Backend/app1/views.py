from TimeProject.settings import domain_url,app_id,app_secret,order_url,notify_url
import urllib.request, urllib.parse
import json
from django.shortcuts import render, HttpResponse, redirect
import os.path
import time
from TimeProject.settings import BASE_DIR, MEDIA_ROOT
from app1.models import Article1, Article_category1, Product, \
    Product_categories, User, Trade, ImgName, ClientForms, ReceiveEmail, adminUser
from app1.utils import expand, list_to_model, product_cat_list_to_model, \
    htmlToWxml, getWxPayOrdrID, get_bodyData, trans_xml_to_dict, get_paysign, priceToInt, intToPrice
import math
from decimal import Decimal
import base64
import requests
from datetime import datetime
from app1.sendmail import send_email_async
from pprint import pprint

def index(request):
    if request.method == "GET":
        return render(request, 'adminLogin.html')
    if request.method == 'POST':
        data = request.POST
        if adminUser.objects.filter(username=data['zyys']) \
                and adminUser.objects.get(username=data['zyys']).password == data['hidden_password']:
            request.session.set_expiry(0)
            request.session['loged'] = True
            return redirect('/wx_mini/index')
        else:
            return render(request, 'adminLogin.html', {'err_msg': True})

def trueIndex(req):
    if not req.session.get('loged'):
        return HttpResponse("未登录")
    else:
        return render(req, 'index.html')

# def api_test(request):
#     openid = request.session.get("openid")
#     data = json.dumps([
#         {"index": 1, "name": "hello"},
#         {"index": 2, "name": "world"},
#         {"index": 3, "name": "!"},
#     ])
#     print(openid)
#     return HttpResponse(data, content_type="application/json")

def code2status(request):
    #print(request.COOKIES)

    #print("js_code from wechat client: ", request.GET['code'])
    data = urllib.parse.urlencode([
        ('appid', app_id),
        ('secret', app_secret),
        ('js_code', request.GET['code']),
        ('grant_type', 'authorization_code'),
    ])
    code2SessionUrl = "https://api.weixin.qq.com/sns/jscode2session?%s" % data
    code2SessionResponseData = ""
    with urllib.request.urlopen(code2SessionUrl) as f:
        code2SessionResponseData = f.read().decode('utf-8')
    code2SessionResponseData = json.loads(code2SessionResponseData) # str转换为dict
    # print(code2SessionResponseData)
    session_key = code2SessionResponseData['session_key']
    open_id = code2SessionResponseData['openid']
    user = User.objects.get_or_create(openid=open_id)[0]
    if user.session_key != session_key:
        user.session_key = session_key
        user.save()
    request.session['openid'] = open_id
    return HttpResponse("获取code成功")

def demo(req):
    htmlData = ''
    if req.method == "POST":
        htmlData = req.POST['content1']
    return render(req, 'demo.html', {"htmlData": htmlData})

def upload(req):
    #print("get: ", req.GET, "============\n")
    #print("post: ", req.POST, "============\n")
    #print("files: ", req.FILES, "============\n")
    #print("imgFile: ", req.FILES['imgFile'], "============\n")
    #print("imgFile: ", type(req.FILES['imgFile']), "============\n")

    str_now_time = str(round(time.time() * 1000))  # 引入毫秒级时间戳，防止重复
    file_name = req.FILES['imgFile'].name
    dealt_file_name = str_now_time + "_" + file_name
    file_path = os.path.join(BASE_DIR, 'static', 'img', dealt_file_name)
    upload_file = req.FILES['imgFile']
    with open(file_path, 'wb') as f:
        f.write(upload_file.read())
    returned_data = json.dumps({
        "error" : 0,
        "url" : domain_url + '/wx_mini/getProjectImg/' + dealt_file_name
    })
    return HttpResponse(content=returned_data, content_type='application/json')

def getProjectImg(req, filename):
    imgData = None
    try:
        f = open(os.path.join(MEDIA_ROOT, filename), "rb")
        imgData = f.read()
        f.close()
    except Exception as e:
        #print(e)
        return HttpResponse("example提醒您：没有这张图片哦", status='404')
    return HttpResponse(content=imgData, content_type='image/'+ filename.split(".")[-1])

#添加文章
def appendArticle(req):
    articleData = json.loads(req.POST['articleData'])

    img = articleData['img']
    imgdata = articleData['img'].split("base64,")[1]  # 二进制base64图片数据
    str_now_time = str(round(time.time() * 1000))
    postfix = "."+ img[img.find("/")+1: img.find(";")]
    imgFilePath = os.path.join(MEDIA_ROOT, str_now_time + postfix)

    with open(imgFilePath, "wb") as f:
        f.write(base64.b64decode(imgdata))
    article = Article1.objects.create(
        title = articleData['title'],
        author = articleData['author'],
        time = articleData['time'],
        img = "/wx_mini/getProjectImg/" + str_now_time + postfix,
        _from = articleData['from'],
        digest = articleData['digest'],
        content = articleData['content'],
        show = int(articleData['articleStatus']),
        category = Article_category1.objects.get(id=articleData['category'][-1]),
    )
    article.order = article.id  # 顺序值默认等于id
    article.save()
    return HttpResponse('ok')

#获取文章分类
def getClassifyArticle(req):
    Article_category1.objects.get_or_create(name="未分类")[0]  # 添加一个未分类
    ArticleClassesData = json.dumps(Article_category1.to_JSON_form(None))
    return HttpResponse(content=ArticleClassesData, content_type='application/json')

#更新文章分类
def refreshClassifyArticle(req):
    ArticleClassesData = json.loads(req.POST['options'])
    Article_categories = Article_category1.objects.all()

    # 删除部分
    exist_node_id = expand(ArticleClassesData) # 所有数据库和前端传回的同时存在的分类的id
    for child_node in Article_categories:
        if child_node.id not in exist_node_id:
            child_node.delete()
            # #保护性"删除"
            # child_node.level = 0
            # child_node.father = None
            # child_node.save()

    # 增加和修改
    for level_1_list_node in ArticleClassesData:
        current_node = None
        if not level_1_list_node.get('level'):  # 说明是才添加的一级分类
            current_node = Article_category1.objects.create(
                name=level_1_list_node['label'],
            )
        else:
            current_node = Article_category1.objects.get(id=int(level_1_list_node['id']))
            if current_node.name != level_1_list_node['label']:
                current_node.name = level_1_list_node['label']
        current_node.level = 1
        current_node.father = None
        current_node.save()
        list_to_model(level_1_list_node, current_node)

    return HttpResponse("ok")

#获取文章列表
def getArticleListData(req):
    category_array = json.loads(req.GET['category_array'])
    show = int(req.GET['show'])
    all_articles = []
    if category_array[0] == 0:
        all_articles = Article1.objects.filter(show=show).order_by('order')
    else:
        last_category_id = category_array[-1]
        # 找出last_category_id的id号和所有子分类的id号
        category_and_descendant_array = \
            Article_category1.objects.get(id=last_category_id).get_self_and_descendant_node_id()
        #print(category_and_descendant_array)
        for category_id in category_and_descendant_array:
            this_category_articles_set = Article_category1.objects.get(id=category_id).article1_set.filter(show=show)
            for article in this_category_articles_set:
                all_articles.append(article)
        # 排序,按order
        all_articles = sorted(all_articles, key=lambda a: a.order)

    data = []
    for article in all_articles:
        self_and_ancestor_node_id = article.category.get_self_and_ancestor_node_id()
        category_text = ""
        for category_id in self_and_ancestor_node_id:
            category_node = Article_category1.objects.get(id=category_id)
            category_text += (category_node.name + " / ")
        category_text = category_text[:-2]
        data.append({
            'title': article.title,
            'category_text': category_text,
            'order': article.order,
            'time': article.time,
            'id': article.id
        })
    data = json.dumps(data)
    return HttpResponse(content_type='application/json', content=data)

#更改show为1
def showArticle(req):
    id = req.POST['id']
    article = Article1.objects.get(id=int(id))
    article.show = 1
    article.save()
    return HttpResponse("ok")

#更改show为2
def hideArticle(req):
    id = req.POST['id']
    article = Article1.objects.get(id=int(id))
    article.show = 2
    article.save()
    return HttpResponse("ok")

#更改show为3
def deleteArticle(req):
    id = req.POST['id']
    article = Article1.objects.get(id=int(id))
    article.show = 3
    article.save()
    return HttpResponse("ok")

#保存文章顺序
def storeArticleOrder(req):
    #print(req.POST['data'])
    data = json.loads(req.POST['data'])
    for list_article in data:
        article = Article1.objects.get(id=list_article['id'])
        article.order = list_article['order']
        article.save()
    return HttpResponse("ok")

#通过id获取文章
def getArticleById(req):
    #print(req.GET)
    article = Article1.objects.get(id=int(req.GET['id']))

    data = {
        "title": article.title,
        "category": article.category.get_self_and_ancestor_node_id(),
        "author": article.author,
        "time": article.time,
        "img": article.img,
        "articleStatus": str(article.show),
        "from": article._from,
        "digest": article.digest,
        "content": article.content,

        "id": article.id,
    }
    return HttpResponse(content=json.dumps(data),content_type='application/json')

#修改文章内容
def changeArticle(req):
    articleData = json.loads(req.POST['articleData'])

    img = articleData['img']
    imgdata = None
    str_now_time = str(round(time.time() * 1000))
    postfix = "." + img[img.find("/") + 1: img.find(";")]
    imgFilePath = os.path.join(MEDIA_ROOT, str_now_time + postfix)

    if img.startswith("data:image"):  # 说明修改了图片，如果img是文件名就没有修改
        imgdata = articleData['img'].split("base64,")[1]
        with open(imgFilePath, "wb") as f:
            f.write(base64.b64decode(imgdata))

    #  获取文章
    article = Article1.objects.get(id=int(articleData['id']))
    #  修改文章
    article.title = articleData['title']
    article.author = articleData['author']
    article.time = articleData['time']
    if img.startswith("data:image"):
        article.img = "/wx_mini/getProjectImg/" + str_now_time + postfix
    article._from = articleData['from']
    article.digest = articleData['digest']
    article.content = articleData['content']
    article.show = int(articleData['articleStatus'])
    article.category = Article_category1.objects.get(id=articleData['category'][-1])

    article.save()
    return HttpResponse("ok")

#添加产品
def uploadProduct(req):
    productData = json.loads(req.POST['productData'])
    try:
        float(productData['price'])
        float(productData['originPrice'])
    except:
        return HttpResponse(status=404, content="价格必须为数字")

#保存图片
    img = productData['img']
    if img:
        imgdata = productData['img'].split("base64,")[1]  # 二进制base64图片数据
        str_now_time = str(round(time.time() * 1000))
        postfix = "." + img[img.find("/") + 1: img.find(";")]
        imgFilePath = os.path.join(MEDIA_ROOT, str_now_time + postfix)

        with open(imgFilePath, "wb") as f:
            f.write(base64.b64decode(imgdata))

    product = Product.objects.create(
        name=productData['name'],
        category = Product_categories.objects.get(id=productData['category'][-1]),
        time = productData['time'],
        img = "/wx_mini/getProjectImg/" + str_now_time + postfix if img else '',
        digest = productData['digest'],
        content = productData['content'],
        price = productData['price'],
        origin_price = productData['originPrice'],
        show = productData['productStatus'],
    )
    product.order = product.id  # 顺序值默认等于id
    product.save()
    return HttpResponse('ok')

#获取产品分类
def getClassifyProduct(req):
    Product_categories.objects.get_or_create(name="未分类")[0]  # 添加一个未分类
    ProductClassesData = json.dumps(Product_categories.to_JSON_form(None))
    return HttpResponse(content=ProductClassesData, content_type='application/json')

#更新产品分类
def refreshClassifyProduct(req):
    ProductClassesData = json.loads(req.POST['options'])
    Product_categories_all = Product_categories.objects.all()

    # 删除部分
    exist_node_id = expand(ProductClassesData)  # 所有数据库和前端传回的同时存在的分类的id
    for child_node in Product_categories_all:
        if child_node.id not in exist_node_id:
            child_node.delete()
            # #保护性"删除"
            # child_node.level = 0
            # child_node.father = None
            # child_node.save()

    # 增加和修改
    for level_1_list_node in ProductClassesData:
        current_node = None
        if not level_1_list_node.get('level'):  # 说明是才添加的一级分类
            current_node = Product_categories.objects.create(
                name=level_1_list_node['label'],
            )
        else:
            current_node = Product_categories.objects.get(id=int(level_1_list_node['id']))
            if current_node.name != level_1_list_node['label']:
                current_node.name = level_1_list_node['label']
        current_node.level = 1
        current_node.father = None
        current_node.save()
        product_cat_list_to_model(level_1_list_node, current_node)

    return HttpResponse("ok")

#获取产品列表
def getProductListData(req):
    category_array = json.loads(req.GET['category_array'])
    show = int(req.GET['show'])
    all_products = []
    if category_array[0] == 0:
        all_products = Product.objects.filter(show=show).order_by('order')
    else:
        last_category_id = category_array[-1]
        # 找出last_category_id的id号和所有子分类的id号
        category_and_descendant_array = \
            Product_categories.objects.get(id=last_category_id).get_self_and_descendant_node_id()
        #print(category_and_descendant_array)
        for category_id in category_and_descendant_array:
            this_category_products_set = Product_categories.objects.get(id=category_id).product_set.filter(show=show)
            for product in this_category_products_set:
                all_products.append(product)
        # 排序,按order
        all_products = sorted(all_products, key=lambda a: a.order)

    data = []
    #print(all_products)
    for product in all_products:
        #print(product)
        self_and_ancestor_node_id = product.category.get_self_and_ancestor_node_id()
        category_text = ""
        for category_id in self_and_ancestor_node_id:
            category_node = Product_categories.objects.get(id=category_id)
            category_text += (category_node.name + " / ")
        category_text = category_text[:-2]
        data.append({
            'title': product.name,
            'category_text': category_text,
            'order': product.order,
            'time': product.time,
            'id': product.id
        })
    data = json.dumps(data)
    return HttpResponse(content_type='application/json', content=data)

#更改show为1
def showProduct(req):
    id = req.POST['id']
    article = Product.objects.get(id=int(id))
    article.show = 1
    article.save()
    return HttpResponse("ok")

#更改show为2
def hideProduct(req):
    id = req.POST['id']
    article = Product.objects.get(id=int(id))
    article.show = 2
    article.save()
    return HttpResponse("ok")

#更改show为3
def deleteProduct(req):
    id = req.POST['id']
    article = Product.objects.get(id=int(id))
    article.show = 3
    article.save()
    return HttpResponse("ok")

#保存产品顺序
def storeProductOrder(req):
    #print(req.POST['data'])
    data = json.loads(req.POST['data'])
    for list_product in data:
        article = Product.objects.get(id=list_product['id'])
        article.order = list_product['order']
        article.save()
    return HttpResponse("ok")

#通过id获取产品信息
def getProductById(req):
    #print(req.GET)
    product = Product.objects.get(id=int(req.GET['id']))

    data = {
        "name": product.name,
        "category": product.category.get_self_and_ancestor_node_id(),
        "time": product.time,
        "img": product.img,
        "digest": product.digest,
        "content": product.content,
        "price": product.price,
        'originPrice': product.origin_price,
        "productStatus": str(product.show),

        "id": product.id,
    }
    return HttpResponse(content=json.dumps(data),content_type='application/json')

#修改产品信息
def changeProduct(req):
    productData = json.loads(req.POST['productData'])
    try:
        float(productData['price'])
        float(productData['originPrice'])
    except:
        return HttpResponse(status=404, content="价格必须为数字")

#保存图片 if 图片更改了
    img = productData['img']
    imgdata = None
    str_now_time = str(round(time.time() * 1000))
    postfix = "." + img[img.find("/") + 1: img.find(";")]
    imgFilePath = os.path.join(MEDIA_ROOT, str_now_time + postfix)

    if img.startswith("data:image"):  # 说明修改了图片，如果img是文件名就没有修改
        imgdata = productData['img'].split("base64,")[1]
        with open(imgFilePath, "wb") as f:
            f.write(base64.b64decode(imgdata))

    #  获取产品
    product = Product.objects.get(id=int(productData['id']))
    #  修改产品
    product.name = productData['name']
    product.category = Product_categories.objects.get(id=productData['category'][-1])
    product.time = productData['time']
    if img.startswith("data:image"):
        product.img = "/wx_mini/getProjectImg/" + str_now_time + postfix
    product.digest = productData['digest']
    product.content = productData['content']
    product.price = productData['price']
    product.origin_price = productData['originPrice']
    product.show = int(productData['productStatus'])

    product.save()
    return HttpResponse("ok")

#客户端获取某类文章列表 默认6条
def getArticleListClient(req):
    categoryId = int(req.GET['categoryId'])
    page = int(req.GET['page'])
    articles = Article1.objects.filter(category_id=categoryId, show=1).order_by('-order')
    current_page_articles = articles[(page - 1) * 6: min(page * 6, len(articles))]
    articles_list = []
    #id,img,title,time,digest(40)
    for article in current_page_articles:
        articles_list.append({
            "id": article.id,
            "img": article.img,
            "title": article.title,
            "time": article.time.split()[0],
            "digest": article.digest[:40] + "......"
        })
    data = {
        "total": len(articles),
        "pages": math.ceil(len(articles)/6) if len(articles) else 0,
        "currentPage": page if len(articles) else 0,
        "articles": articles_list
    }
    return  HttpResponse(content=json.dumps(data), content_type="application/json")

#客户端获取某类产品列表 默认5条
def getProductListClient(req):
    categoryId = int(req.GET['categoryId'])
    page = int(req.GET['page'])
    products = Product.objects.filter(category_id=categoryId, show=1).order_by('-order')
    current_page_products = products[(page - 1) * 5: min(page * 5, len(products))]
    products_list = []
    # id,img,name,price
    for product in current_page_products:
        products_list.append({
            "id": product.id,
            "img": product.img,
            "name": product.name,
            "price": str(Decimal(product.price).quantize(Decimal("0.00")))
        })
    data = {
        "total": len(products),
        "pages": math.ceil(len(products) / 5) if len(products) else 0,
        "currentPage": page if len(products) else 0,
        "products": products_list
    }
    return HttpResponse(content=json.dumps(data), content_type="application/json")

def getArticleByIdClient(req):
    article = Article1.objects.get(id=int(req.GET['id']))

    data = {
        "title": article.title,
        "time": article.time,
        "digest": article.digest,
        "content": article.content,
        "img": article.img
    }
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def getProductByIdClient(req):
    product = Product.objects.get(id=int(req.GET['id']))
    data = {
        "name": product.name,
        "img": product.img or "/wx_mini/getProjectImg/default_pic.jpg",
        "content": product.content,
        "price": str(Decimal(product.price).quantize(Decimal("0.00"))),
        "id": product.id,
    }
    return HttpResponse(content=json.dumps(data), content_type='application/json')

#客户端上传文件，比如个人中心的资料上传，还有药品代购的图片上传
def uploadFileClient(req):
    #print("上传文件")
    #print(time.time())
    file_name = list(req.FILES.keys())[0]
    upload_file = req.FILES[file_name]
    suffix = upload_file.name.split(".")[-1]
    file_path = os.path.join(BASE_DIR, 'static', 'img', file_name + '.' + suffix)
    ImgName.objects.create(img_name=file_name,img_name_with_suffix=file_name+'.'+suffix)
    with open(file_path, 'wb') as f:
        f.write(upload_file.read())
    #print(time.time())
    return HttpResponse("ok")

#客户端提交表单资料，图片资料只有不包括后缀的文件名
def submitFormsClient(req):
    types = req.POST['types']
    openid = req.session['openid']
    data_json_str = req.POST['data']
    ClientForms.objects.create(
        types = types,
        other_fields = data_json_str,
        openid = openid
    )
    content = '''
            <p>用户id为:<strong>%s</strong></p>
            <p>提交了类型为:<strong>%s</strong></p>
            <p>的表单信息，请前往后台处理。</p>
        ''' % (openid, types)

    send_email_async(content=content, to_account=ReceiveEmail.objects.first().email,
                     manage_url=domain_url + "/wx_mini/")
    return HttpResponse("ok")

def getArticleListByOpenIdClient(req):
    openid = req.session['openid']
    categoryId = int(req.GET['categoryId'])
    page = int(req.GET['page'])
    articles = Article1.objects.filter(category_id=categoryId, show=1, author=openid).order_by('-order')
    current_page_articles = articles[(page - 1) * 3: min(page * 3, len(articles))]
    articles_list = []
    #id,img,title,time,digest(40)
    for article in current_page_articles:
        articles_list.append({
            "id": article.id,
            "img": article.img,
            "title": article.title,
            "time": article.time.split()[0],
            "digest": article.digest[:40] + "......"
        })
    data = {
        "total": len(articles),
        "pages": math.ceil(len(articles)/3) if len(articles) else 0,
        "currentPage": page if len(articles) else 0,
        "articles": articles_list
    }
    return  HttpResponse(content=json.dumps(data), content_type="application/json")

def getTel(req):
    openid = req.session['openid']
    user = User.objects.get(openid=openid)
    tel = user.telephone
    data = {
        'tel': tel
    }
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def changeTel(req):
    openid = req.session['openid']
    tel = req.POST['data']
    user = User.objects.get(openid=openid)
    user.telephone = tel
    user.save()
    return HttpResponse("ok")

#小程序请求预下单，对应动作为跳转到确认订单界面。如果在用户中心里面，则是为了获取信息到小程序全局变量里面，
# 然后直接跳转支付界面
def launchOrder(req):
    req_data = json.loads(req.POST['data'])
    openid = req.session['openid']
    user = User.objects.get(openid=openid)
    data = {}
    if not user.telephone:
        data = {"success": False, "mes_data": "没有设置手机号码", "error_code": 1}
        return HttpResponse(content=json.dumps(data),content_type="application/json")
    now_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount = req_data['amount']
    product_id = req_data['product_id']
    product = Product.objects.get(id=product_id)
    int_total_price = int(priceToInt(product.price)) * amount  # 单位:分
    total_price = intToPrice(str(int_total_price))  # 单位:元
    img = product.img
    #time, amount, total_price, product_id, img
    data = {
        "time": now_datetime,
        "amount": amount,
        "total_price": total_price,
        "product_id": product_id,
        "img": img
    }

    return HttpResponse(content=json.dumps(data), content_type="application/json")

#服务器端生成订单，并返回订单信息，对应动作为跳转到支付界面
def true_launch_order(req):
    # req_data包含product_id, amount, total_price，liuyan # 留言
    req_data = json.loads(req.POST['data'])
    if not req_data:
        data = {
            "success": False,
            "mes_data": "提交失败,请稍后再试",
            "error_code": 1
        }
        return HttpResponse(content=json.dumps(data), content_type='application/json')
    openid = req.session['openid']
    user = User.objects.get(openid=openid)
    product_id = req_data['product_id']
    product = Product.objects.get(id=product_id)
    amount = int(req_data['amount'])

    liuyan = req_data['liuyan']

    int_total_price = int(priceToInt(product.price)) * amount  # 单位:分
    total_price = intToPrice(str(int_total_price))  # 单位:元,计算出来返回给小程序

    trade = Trade.objects.create(
        oid=getWxPayOrdrID(),  # 编号
        users=openid,       # 用户名
        product=product,    # 产品外键
        product_name=product.name, # 产品名
        amount=amount,  # 数量
        price= priceToInt(product.price), # 单价(单位：分)
        phone=user.telephone,   # 电话号码
        message=liuyan,             # 备注留言
        total_price = str(int_total_price),  # 总价(单位：分)
        money_status = 1, # 订单状态  1为未付款 2为已付款 3为已退款
        trade_status = 1, # 订单状态  1为未处理 2为配送中 3为已发货 4为已收货 5已完成 6为用户取消订单
        show = 1# 2为被用户删除, 1为没被删除 管理员始终可见
    )

    data = {
        "success": True,
        "total_price": total_price,
        "trade_id": str(trade.oid)
    }

    content = '''
            <p>用户id为:<strong>%s</strong></p>
            <p>提交了订单号为:<strong>%s</strong></p>
            <p>的订单,请前往后台联系用户付款。</p>
        ''' % (openid, trade.oid)

    send_email_async(content=content, to_account=ReceiveEmail.objects.first().email,
                     manage_url=domain_url + "/wx_mini/")

    return HttpResponse(content=json.dumps(data), content_type='application/json')

#统一下单支付接口
def payOrder(request):
    req_data = json.loads(request.POST['data'])
    trade_id = req_data['trade_id']
    #print("统一下单订单号：", trade_id)
    trade = Trade.objects.get(oid=int(trade_id))
    openid = request.session['openid']
    product = trade.product
    body = "卓越壹生-" + product.name
    out_trade_no = trade.oid
    if trade.total_price == "0":
        data = {
            "success": False,
            "err_code": 1,
            "msg_data": "当前订单金额为0,无法支付,请等待管理员与您联系改价后再支付"
        }
        return HttpResponse(content=json.dumps(data), content_type="application/json")
    if request.method == 'POST':
        # 获取价格
        price = trade.total_price
        # 获取客户端ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        print("\n",ip,"\n")
        client_ip = ip.split(":")[0]
        # 获取小程序openid
        openid = openid
        # 请求微信的url
        url = order_url
        # 拿到封装好的xml数据
        body_data = get_bodyData(openid, client_ip, price, body, notify_url, out_trade_no)
        # 获取时间戳
        timeStamp = str(int(time.time()))
        # 请求微信接口下单
        respone = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
        # 回复数据为xml,将其转为字典
        content = trans_xml_to_dict(respone.content)
        #print(content)
        if content["return_code"] == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content.get("prepay_id")
            # 获取随机字符串
            nonceStr = content.get("nonce_str")
            # 获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign = get_paysign(prepay_id, timeStamp, nonceStr)
            # 封装返回给前端的数据
            data = {"success": True,"package": "prepay_id=" + prepay_id, "nonceStr": nonceStr, "paySign": paySign, "timeStamp": timeStamp}
            return HttpResponse(content=json.dumps(data), content_type='application/json')
        else:
            return HttpResponse("请求支付失败",status=404)
    else:
        return HttpResponse(content="请求方法错误",status=404)

#微信通知支付结果
# def wx_pay_notify_url(req):
#     # content = '''
#     #                 <p>用户id为:<strong>%s</strong></p>
#     #                 <p><span style='color:red'>支付</span>了订单号为:<strong>%s</strong></p>
#     #                 <p>的订单,请及时联系用户进行服务，用户的手机号为:<span style='color:red'>%s</span>。</p>
#     #             ''' % (openid, trade.oid, trade.phone)
#     #
#     # send_email_async(content=content, to_account=ReceiveEmail.objects.first().email,
#     #                  manage_url=domain_url + "/wx_mini/")
#     return HttpResponse("ok")

def wx_pay_notify_url(request):
    import xml.etree.ElementTree as et
    _xml = request.body
    #拿到微信发送的xml请求 即微信支付后的回调内容
    xml = str(_xml, encoding="utf-8")
    #print("xml", xml)
    return_dict = {}
    tree = et.fromstring(xml)
    #xml 解析
    return_code = tree.find("return_code").text
    try:
        if return_code == 'FAIL':
            # 官方发出错误
            return_dict['message'] = '支付失败'
            #return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
        elif return_code == 'SUCCESS':
            _out_trade_no = tree.find("out_trade_no").text  #拿到自己这次支付的 out_trade_no
            trade = Trade.objects.get(oid=_out_trade_no)  #这里省略了 拿到订单号后的操作 看自己的业务需求
            trade.notify_status = 3
            trade.save()
    except Exception as e:
        pass
    finally:
        return HttpResponse('''
        <xml>
            <return_code><![CDATA[SUCCESS]]></return_code>
            <return_msg><![CDATA[OK]]></return_msg>
        </xml>
        ''', status=200)


#小程序用户确认支付,更改订单状态
def paySuccess(req):
    openid = req.session['openid']
    req_data = json.loads(req.POST['data'])
    trade_id = req_data['trade_id']
    trade = Trade.objects.get(oid=int(trade_id))
    trade.money_status = 2
    trade.trade_status = 2
    trade.pay_time = datetime.now()
    trade.save()

    content = '''
                <p>用户id为:<strong>%s</strong></p>
                <p><span style='color:red'>支付</span>了订单号为:<strong>%s</strong></p>
                <p>的订单,请及时联系用户进行服务，用户的手机号为:<span style='color:red'>%s</span>。</p>
            ''' % (openid, trade.oid, trade.phone)

    send_email_async(content=content, to_account=ReceiveEmail.objects.first().email,
                     manage_url=domain_url + "/wx_mini/")

    return HttpResponse("ok")

def getTradeNumbers(req):
    openid = req.session['openid']
    trades = Trade.objects.filter(users=openid, show=1)
    data = {
        "weizhifu": len(trades.filter(trade_status=1)),
        "daishouhuo": len(trades.filter(trade_status=2)),
        "yiwancheng": len(trades.filter(trade_status=3)),
    }
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def getTradeListClient(req):
    trade_status = int(req.GET['trade_status'])
    page = int(req.GET['page'])
    openid = req.session['openid']

    if trade_status == 0:
        trades = Trade.objects.filter(show=1, users=openid).order_by('-order_time')
    else:
        trades = Trade.objects.filter(trade_status=trade_status,show=1, users=openid).order_by("-order_time")
    current_page_trades = trades[(page - 1) * 6: min(page * 6, len(trades))]
    trades_list = []
    # trade_id,time,amount,product_name,trade_status,total_price,trade_status_text
    for trade in current_page_trades:
        # 1为未处理(未付款)2为待收货(待收货)3为已收货(已收货)4已退款(管理员设置)(所有订单)
        if trade.trade_status == 1:
            trade_status_text = "未付款"
        elif trade.trade_status == 2:
            trade_status_text = "待收货"
        elif trade.trade_status == 3:
            trade_status_text = "已完成"
        else:
            trade_status_text = "已退款"
        trades_list.append({
            'trade_id': trade.oid,
            'time': trade.order_time.strftime( '%Y-%m-%d %H:%M:%S'),
            'amount': trade.amount,
            'product_name': trade.product_name,
            'trade_status': trade.trade_status,
            'total_price': intToPrice(trade.total_price),
            'trade_status_text': trade_status_text
        })
    data = {
        "total": len(trades),
        "pages": math.ceil(len(trades) / 6) if len(trades) else 0,
        "currentPage": page if len(trades) else 0,
        "trades": trades_list
    }
    return HttpResponse(content=json.dumps(data), content_type="application/json")

def getTradeDetailsByIdClient(req):
    openid = req.session['openid']
    trade_id = req.GET['trade_id']

    trade = Trade.objects.get(oid=trade_id)
    if openid != trade.users:
        return HttpResponse("不是你的订单", status=404)

    if trade.trade_status == 1:
        trade_status_text = "未付款"
    elif trade.trade_status == 2:
        trade_status_text = "待收货"
    elif trade.trade_status == 3:
        trade_status_text = "已完成"
    else:
        trade_status_text = "已退款"
    data = {
        "trade_id": trade_id,
        "order_time": trade.order_time.strftime( '%Y-%m-%d %H:%M:%S'),
        "pay_time": trade.pay_time.strftime( '%Y-%m-%d %H:%M:%S') if trade.pay_time else "未支付",
        "liuyan": trade.message,

        "trade_status": trade.trade_status,
        "trade_status_text": trade_status_text,

        "total_price": intToPrice(trade.total_price),
        "tel": trade.phone,

        "product_id": trade.product.id,
        "product_img": trade.product.img or "/wx_mini/getProjectImg/default_pic.jpg",
        "product_name": trade.product.name,
        "amount": trade.amount,
        "product_price": intToPrice(trade.price)
    }

    # trade_id: "20181205030420942869",
    # order_time: "2018-12-5 22:27:18",
    # pay_time: "2018-12-5 22:36:25",
    # liuyan: "搞快点，臭弟弟", // 留言备注
    #
    # trade_status: 2,
    # trade_status_text: "待收货",
    #
    # total_price: "0.02", // 实付款
    # tel: "example", // 电话
    #
    # product_id: "51",
    # product_img: "/wx_mini/getProjectImg/1543949209560.png",
    # product_name: "1分钱的东西",
    # amount: "2",
    # product_price: "0.01",
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def remindUs(req):
    openid = req.session['openid']
    trade_id = req.GET['trade_id']

    content = '''
        <p>用户id为:<strong>%s</strong></p>
        <p>订单号为:<strong>%s</strong></p>
        <p>的订单，提醒您发货了。</p>
    ''' % (openid, trade_id)

    send_email_async(content=content, to_account=ReceiveEmail.objects.first().email,
                     manage_url=domain_url+"/wx_mini/")
    return HttpResponse(content_type='application/json', content=json.dumps({
        "success": True
    }))

def deleteTradeClient(req):
    openid = req.session['openid']
    trade_id = req.GET['trade_id']
    trade = Trade.objects.get(users=openid, oid=trade_id)
    trade.show = 2
    trade.save()
    return HttpResponse(content_type='application/json', content=json.dumps({
        "success": True
    }))

def sureTradeClient(req):
    openid = req.session['openid']
    trade_id = req.GET['trade_id']
    trade = Trade.objects.get(users=openid, oid=trade_id)
    trade.trade_status = 3
    trade.save()
    return HttpResponse(content_type='application/json', content=json.dumps({
        "success": True
    }))

def getTradeListData(req):
    searchTel = req.GET.get('searchTel')
    searchOpenid = req.GET.get('searchOpenid')
    #print(searchTel, searchOpenid)
    if searchTel:
        all_trades = Trade.objects.filter(show=1, phone=searchTel).order_by("-order_time")
    elif searchOpenid:
        all_trades = Trade.objects.filter(show=1, users=searchOpenid).order_by("-order_time")
    else:
        all_trades = Trade.objects.filter(show=1).order_by("-order_time")
    data = []
    for trade in all_trades:
        if trade.trade_status == 1:
            trade_status_text = "未付款"
        elif trade.trade_status == 2:
            trade_status_text = "待收货"
        elif trade.trade_status == 3:
            trade_status_text = "已完成"
        else:
            trade_status_text = "已退款"
        data.append({
            "oid": trade.oid,
            "openid": trade.users,
            "phone": trade.phone,
            "total_price": intToPrice(trade.total_price),
            "order_time": trade.order_time.strftime( '%Y-%m-%d %H:%M:%S'),
            "trade_status_text": trade_status_text,
            "pay_time": trade.pay_time.strftime( '%Y-%m-%d %H:%M:%S') if trade.pay_time else "未支付",
        })
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def getTradeDetailsById(req):
    trade_id = req.GET['trade_id']

    trade = Trade.objects.get(oid=trade_id)

    # if trade.trade_status == 1:
    #     trade_status_text = "未付款"
    # elif trade.trade_status == 2:
    #     trade_status_text = "待收货"
    # elif trade.trade_status == 3:
    #     trade_status_text = "已完成"
    # else:
    #     trade_status_text = "已退款"

    int_total_price = int(priceToInt(trade.product.price)) * trade.amount  # 计算原价
    cal_total_price = intToPrice(str(int_total_price))  # 单位:元,计算出来原总价返回后台

    data = {
        "trade_id": trade_id,
        'openid': trade.users,
        "tel": trade.phone,
        "order_time": trade.order_time.strftime( '%Y-%m-%d %H:%M:%S'),
        "pay_time": trade.pay_time.strftime( '%Y-%m-%d %H:%M:%S') if trade.pay_time else "未支付",
        "liuyan": trade.message,
        "trade_status": trade.trade_status,
        "now_total_price": intToPrice(trade.total_price),

        "product_img": trade.product.img,
        "product_name": trade.product.name,
        "amount": trade.amount,
        "product_price": intToPrice(trade.price),
        "cal_total_price": cal_total_price
    }

    # trade_id: "20181205030420942869",
    # order_time: "2018-12-5 22:27:18",
    # pay_time: "2018-12-5 22:36:25",
    # liuyan: "搞快点，臭弟弟", // 留言备注
    #
    # trade_status: 2,
    # trade_status_text: "待收货",
    #
    # total_price: "0.02", // 实付款
    # tel: "example", // 电话
    #
    # product_id: "51",
    # product_img: "/wx_mini/getProjectImg/1543949209560.png",
    # product_name: "1分钱的东西",
    # amount: "2",
    # product_price: "0.01",
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def changeTradeData(req):
    data = json.loads(req.POST['data'])
    changePrice = data['changePrice']
    new_trade_status = data['trade_status']
    # print(data)
    oid = data['oid']

    trade = Trade.objects.get(oid=oid)
    trade.trade_status = new_trade_status
    trade.save()

    data['success'] = True
    if not changePrice == "0.00":
        int_new_trade_status = priceToInt(changePrice) # 单位为分的字符串，修改价格
        cal_new_price = Decimal(trade.total_price) + Decimal(int_new_trade_status)
        data = {}
        if cal_new_price <= 0:
            data['success'] = False
            data['err_msg'] = "修改失败，修改后的价格小于等于零"
        else:
            trade.oid = getWxPayOrdrID()  # 新订单号,防止不同价格请求统一下单接口导致失败
            trade.total_price = str(cal_new_price)
            trade.save()
            data['success'] = True

    return HttpResponse(content=json.dumps(data), content_type='application/json')

def deleteTradeData(req):
    oid = req.POST['oid']
    trade = Trade.objects.get(oid=oid)
    trade.show = 3
    trade.save()

    return HttpResponse(content=json.dumps({'success': True}), content_type='application/json')

def getAllTels(req):
    users = User.objects.all()
    tels = []
    for user in users:
        if user.telephone:
            tels.append(user.telephone)
    return HttpResponse(content=json.dumps(tels), content_type='application/json')

def getClienFormLists(req):
    types = req.GET['types']
    msgs = ClientForms.objects.filter(types=types).order_by('-time')
    data = []
    for msg in msgs:
        other_fields = json.loads(msg.other_fields)
        fields = {
            'id': msg.id,
            'openid': msg.openid,
            'time': msg.time.strftime( '%Y-%m-%d %H:%M:%S'),
        }
        msg_data = dict(list(other_fields.items()) + list(fields.items()) )
        if "imageNames" in msg_data.keys() and msg_data['imageNames']:
            former_img_names = msg_data['imageNames']
            msg_data['imageNames'] = []
            for img_name in former_img_names:
                msg_data['imageNames'].append(
                    "/wx_mini/getProjectImg/" +
                    ImgName.objects.get(img_name=img_name).img_name_with_suffix
                )
        if "imageName" in msg_data.keys():
            msg_data['imageName'] = "/wx_mini/getProjectImg/" + \
                ImgName.objects.get(img_name=msg_data['imageName']).img_name_with_suffix
        data.append(msg_data)
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def deleteClienForm(req):
    msg_id = req.POST['msg_id']
    msg_obj = ClientForms.objects.get(id=int(msg_id))
    msg_obj.types = msg_obj.types + "_已删除"
    msg_obj.save()
    return HttpResponse("ok")

def getUserList(req):
    users = User.objects.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'openid': user.openid,
            'tel': user.telephone or "用户暂未设置电话号码"
        })
    return HttpResponse(content=json.dumps(data), content_type='application/json')

def getEmail(req):
    email = ReceiveEmail.objects.first().email
    return HttpResponse(str(email))

def setEmail(req):
    email_obj = ReceiveEmail.objects.first()
    email_obj.email = req.POST['email']
    email_obj.save()

    return HttpResponse(email_obj.email)

def getOpenOrNot(req):
    return HttpResponse('true')

def getTitleText(req):
    return HttpResponse("健康指南")