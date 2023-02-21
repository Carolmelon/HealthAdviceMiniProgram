// pages/productDetail/productDetail.js
const app = getApp();
const WxParse = require('../../wxParse/wxParse.js')
const common = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    product: false,
    url_prefix: app.globalData.url_prefix,
    wxml: null,
    amount: 1,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.showLoading({
      title: '加载中',
    })
    var id = options.id || 48
    'getProductByIdClient'
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getProductByIdClient?id=' + id,
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        // console.log(response)
        this.setData({
          product: response.data,
        })
        wx.hideLoading()
        WxParse.wxParse("wxml", "html", response.data.content, this)
      }
    })
  },

  slider2change(e){
    this.data.amount = e.detail.value
  },

  gotoCashierDesk(){
    var amount = this.data.amount;
    var id = this.data.product.id;
    common.launchTrade(id, amount)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})