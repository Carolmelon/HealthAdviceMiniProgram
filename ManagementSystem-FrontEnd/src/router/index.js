import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/pages/Index'

import AppendArticle from '@/pages/Articles/AppendArticle'    // @代表src文件夹
import ManageArticle from '@/pages/Articles/ManageArticle'
import ClassifyArticle from '@/pages/Articles/ClassifyArticle'
import ArticleHouse from '@/pages/Articles/ArticleHouse'

import ChangeArticle from '@/components/ChangeArticle'

import AddProduct from '@/pages/Products/AddProduct'
import ManageProduct from '@/pages/Products/ManageProduct'
import ClassifyProduct from '@/pages/Products/ClassifyProduct'
import ImportProduct from '@/pages/Products/ImportProduct'
import ManagePdtQuality from '@/pages/Products/ManagePdtQuality'

import ChangeProduct from '@/components/ChangeProduct'

import TradeManage from '@/pages/TradeManage'
import MessageManage from '@/pages/MessageManage'
import MemberManage from '@/pages/MemberManage'
import EmailSet from '@/pages/EmailSet'

import ypdg from '@/pages/messages/ypdg'
import zjyy from '@/pages/messages/zjyy'
import grda from '@/pages/messages/grda'
import zjjy from '@/pages/messages/zjjy'
import tpzl from '@/pages/messages/tpzl'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    //文章开始
    {
      path: '/AppendArticle',
      name: 'AppendArticle',
      component: AppendArticle
    },
    {
      path: '/ManageArticle',
      name: 'ManageArticle',
      component: ManageArticle
    },
    {
      path: '/ClassifyArticle',
      name: 'ClassifyArticle',
      component: ClassifyArticle
    },
    {
      path: '/ArticleHouse',
      name: 'ArticleHouse',
      component: ArticleHouse
    },
    {
      path: '/ChangeArticle',
      name: 'ChangeArticle',
      component: ChangeArticle
    },
    //文章结束
    //产品开始
    {
      path: '/AddProduct',
      name: 'AddProduct',
      component: AddProduct
    },
    {
      path: '/ManageProduct',
      name: 'ManageProduct',
      component: ManageProduct
    },
    {
      path: '/ClassifyProduct',
      name: 'ClassifyProduct',
      component: ClassifyProduct
    },{
      path: '/ImportProduct',
      name: 'ImportProduct',
      component: ImportProduct
    },
    {
      path: '/ManagePdtQuality',
      name: 'ManagePdtQuality',
      component: ManagePdtQuality
    },
    {
      path: '/ChangeProduct',
      name: 'ChangeProduct',
      component: ChangeProduct
    },

    // 订单
//     import TradeManage from '@/pages/TradeManage'
//     import MessageManage from '@/pages/MessageManage'
//     import MemberManage from '@/pages/MemberManage'
//     import EmailSet from '@/pages/EmailSet'
    {
      path: '/TradeManage',
      name: 'TradeManage',
      component: TradeManage
    },
    {
// import ypdg from '@/pages/messages/ypdg'
// import zjyy from '@/pages/messages/zjyy'
// import grda from '@/pages/messages/grda'
// import zjjy from '@/pages/messages/zjjy'
// import tpzl from '@/pages/messages/tpzl'
      path: '/MessageManage',
      name: 'MessageManage',
      component: MessageManage,
      redirect: '/MessageManage/ypdg',
      children: [
        {
          path: 'ypdg',
          component: ypdg
        },
        {
          path: 'zjyy',
          component: zjyy
        },
        {
          path: 'grda',
          component: grda
        },
        {
          path: 'zjjy',
          component: zjjy
        },
        {
          path: 'tpzl',
          component: tpzl
        }
      ]
    },
    {
      path: '/MemberManage',
      name: 'MemberManage',
      component: MemberManage
    },
    {
      path: '/EmailSet',
      name: 'EmailSet',
      component: EmailSet
    },
  ]
})
