from django.db import models

def get_sentinel_category():
    return Article_category1.objects.get_or_create(name="未分类")[0]

def get_sentinel_product_category():
    return Product_categories.objects.get_or_create(name="未分类")[0]

class Article1(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(to='Article_category1',null=True, on_delete=models.SET(get_sentinel_category))
    author = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    img = models.TextField()
    _from = models.CharField(max_length=50)
    digest = models.CharField(max_length=500)
    content = models.TextField()
    show = models.IntegerField(default=1)
    order = models.IntegerField(null=True)
    def __str__(self):
        return str(self.__dict__)

class Article_category1(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    father = models.ForeignKey(to='Article_category1', null=True, on_delete=models.SET_NULL)
    @classmethod
    def FIRST(cls):
        return cls.objects.first()
    def node_to_JSON_form(self):
        return {
            "id": self.id,
            "label": self.name,
            "value": self.id,
            "children": [],
            "level": self.level
        }
    def to_JSON_form(self):
        data = []
        level_is_1 = Article_category1.objects.filter(level=1)
        for node in level_is_1:
            data.append(node.node_to_JSON_form())
        for i in range(len(level_is_1)):
            to_list(level_is_1[i], data[i])
        return data
    def get_self_and_ancestor_node_id(self):
        ids = []
        ids.insert(0, self.id)
        current_node = self
        while(current_node.father):
            ids.insert(0, current_node.father.id)
            current_node = current_node.father
        return ids
    def get_self_and_descendant_node_id(self):
        ids = []
        ids.append(self.id)
        current_node = self
        search_descendant_id(current_node, ids)
        return ids
    def __str__(self):
        return str(self.__dict__)

def to_list(node, list_node):
    all_children_node = node.article_category1_set.all()
    if not all_children_node:
        return
    for child_node in all_children_node:
        child_list_node = child_node.node_to_JSON_form()
        list_node['children'].append(child_list_node)
        to_list(child_node, child_list_node)

def product_cat_to_list(node, list_node):
    all_children_node = node.product_categories_set.all()
    if not all_children_node:
        return
    for child_node in all_children_node:
        child_list_node = child_node.node_to_JSON_form()
        list_node['children'].append(child_list_node)
        product_cat_to_list(child_node, child_list_node)

def search_descendant_id(current_node, ids):
    child_node_set = current_node.article_category1_set.all()
    if not child_node_set:
        return
    for i in child_node_set:
        ids.append(i.id)
        search_descendant_id(i, ids)

def product_search_descendant_id(current_node, ids):
    child_node_set = current_node.product_categories_set.all()
    if not child_node_set:
        return
    for i in child_node_set:
        ids.append(i.id)
        product_search_descendant_id(i, ids)

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(to='Product_categories',null=True, on_delete=models.SET(get_sentinel_product_category))
    time = models.CharField(max_length=50)
    img = models.TextField()
    digest = models.CharField(max_length=500)
    content = models.TextField()
    price = models.CharField(max_length=100)
    origin_price = models.CharField(max_length=100)

    show = models.IntegerField(default=1)
    order = models.IntegerField(null=True)
    def __str__(self):
        return str(self.__dict__)

class Product_categories(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    father = models.ForeignKey(to='Product_categories', null=True, on_delete=models.SET_NULL)
    @classmethod
    def FIRST(cls):
        return cls.objects.first()
    def node_to_JSON_form(self):
        return {
            "id": self.id,
            "label": self.name,
            "value": self.id,
            "children": [],
            "level": self.level
        }
    def to_JSON_form(self):
        data = []
        level_is_1 = Product_categories.objects.filter(level=1)
        for node in level_is_1:
            data.append(node.node_to_JSON_form())
        for i in range(len(level_is_1)):
            product_cat_to_list(level_is_1[i], data[i])  #    需要修改to_list函数
        return data
    def get_self_and_ancestor_node_id(self):
        ids = []
        ids.insert(0, self.id)
        current_node = self
        while(current_node.father):
            ids.insert(0, current_node.father.id)
            current_node = current_node.father
        return ids
    def get_self_and_descendant_node_id(self):
        ids = []
        ids.append(self.id)
        current_node = self
        product_search_descendant_id(current_node, ids)
        return ids
    def __str__(self):
        return str(self.__dict__)

#订单
class Trade(models.Model):
    # 2018000038
    oid = models.CharField(max_length=100, unique=True)  # 编号
    order_time = models.DateTimeField(auto_now_add=True)  # 下单时间
    pay_time = models.DateTimeField(null=True) # 支付时间
    users = models.CharField(max_length=50)   # 用户名
    product = models.ForeignKey(to="Product", on_delete=models.SET_NULL, null=True)  # 产品外键
    product_name = models.CharField(max_length=50)  # 产品名
    amount = models.IntegerField()  # 数量
    price = models.CharField(max_length=50)  # 单价(单位：分)
    phone = models.CharField(max_length=50)  # 电话号码
    message = models.CharField(max_length=100)  # 备注留言
    total_price = models.CharField(max_length=50)  # 总价
    money_status = models.IntegerField()  # 订单状态  1为未付款 2为已付款 (前端返回状态的保存)
    trade_status = models.IntegerField()  # 订单状态  1为未处理(未付款) 2为待发货(待收货) 3为已收货(已收货) 4已退款(管理员设置)(所有订单)
    show = models.IntegerField()   # 2为被用户删除, 1为没被删除，只有未付款的订单可以删除。管理员始终可见
    notify_status = models.IntegerField(default=1) # 1为支付结果没通知到，2为通知到了但支付失败了，3为通知到了且支付成功了

class User(models.Model):
    session_key = models.CharField(max_length=100)
    openid = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50,default='')  # 新增

class ImgName(models.Model):
    img_name = models.CharField(max_length=100)
    img_name_with_suffix = models.CharField(max_length=100)

class ClientForms(models.Model):
    types = models.CharField(max_length=50, blank=False)
    other_fields = models.TextField()
    openid = models.CharField(max_length=100, default="测试")
    time = models.DateTimeField(null=True, auto_now_add=True)

class ReceiveEmail(models.Model):
    email = models.CharField(max_length=50)

class adminUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)