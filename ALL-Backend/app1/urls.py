
from django.contrib import admin
from django.urls import path
from app1.views import index
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.trueIndex),
    path('', index),
    # path('api_test/', views.api_test),
    path('code2status/', views.code2status),
    path('demo', views.demo),
    path('uploadFile', views.upload),
    path('appendArticle', views.appendArticle),
    path('getClassifyArticle', views.getClassifyArticle),
    path('refreshClassifyArticle', views.refreshClassifyArticle),
    path('getArticleListData', views.getArticleListData),
    path('showArticle', views.showArticle),
    path('hideArticle', views.hideArticle),
    path('deleteArticle', views.deleteArticle),
    path('storeArticleOrder', views.storeArticleOrder),
    path('getArticleById', views.getArticleById),
    path('changeArticle', views.changeArticle),

    path('uploadProduct', views.uploadProduct),
    path('getClassifyProduct', views.getClassifyProduct),
    path('refreshClassifyProduct', views.refreshClassifyProduct),
    path('getProductListData', views.getProductListData),
    path('showProduct', views.showProduct),
    path('hideProduct', views.hideProduct),
    path('deleteProduct', views.deleteProduct),
    path('storeProductOrder', views.storeProductOrder),
    path('getProductById', views.getProductById),
    path('changeProduct', views.changeProduct),

    path('getArticleListClient', views.getArticleListClient),
    path("getProductListClient", views.getProductListClient),

    path("getProjectImg/<str:filename>", views.getProjectImg),
    path("getArticleByIdClient", views.getArticleByIdClient),
    path('getProductByIdClient', views.getProductByIdClient),
    path('launchOrder', views.launchOrder),
    path('uploadFileClient', views.uploadFileClient),
    path('submitFormsClient', views.submitFormsClient),
    path('getArticleListByOpenIdClient', views.getArticleListByOpenIdClient),
    path("getTel", views.getTel),
    path("changeTel", views.changeTel),
    path('wx_pay_notify_url', views.wx_pay_notify_url), # 异步通知订单结果,防止前端支付成功以后没有收到通知
    path('trueLaunchOrder', views.true_launch_order), # 创建订单
    path('payMoney', views.payOrder), # 统一支付接口
    path('paySuccess', views.paySuccess), # 前端支付成功以后验证
    path("getTradeNumbers", views.getTradeNumbers), # 获取用户中心的未支付，待发货，待收货数量
    path("getTradeListClient", views.getTradeListClient),
    path("getTradeDetailsByIdClient", views.getTradeDetailsByIdClient),
    path("remindUs", views.remindUs), # 发邮件
    path("deleteTradeClient", views.deleteTradeClient), # 用户删除订单
    path("sureTradeClient", views.sureTradeClient), # 用户确认收货

    path("getTradeListData", views.getTradeListData), # 后台获取trades
    path("getTradeDetailsById", views.getTradeDetailsById),
    path("changeTradeData", views.changeTradeData),
    path("deleteTradeData", views.deleteTradeData),
    path("getAllTels", views.getAllTels),
    path('getClienFormLists', views.getClienFormLists),
    path("deleteClienForm", views.deleteClienForm),
    path("getUserList", views.getUserList),
    path('getEmail', views.getEmail),
    path('setEmail', views.setEmail),
    
    path('getOpenOrNot', views.getOpenOrNot),
    path('getTitleText', views.getTitleText),
]
