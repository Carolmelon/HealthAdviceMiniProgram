// pages/trueUserCenter/trueUserCenter.js
var app = getApp()
var common = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    'weizhifu': 0,
    'daishouhuo': 0,
    "yiwancheng": 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.a = this;
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getTradeNumbers',
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        var data = response.data
        console.log(data)
        this.setData({
          'weizhifu': data.weizhifu,
          'daishouhuo': data.daishouhuo,
          "yiwancheng": data.yiwancheng,
        })
      }
    })
  },
  gototradeList(e){
    var c = e.currentTarget.dataset.category
    wx.navigateTo({
      url: '../tradeList/tradeList?category=' + c,
    })
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
    common.checkTel()  //检查有没有手机号
    console.log("显示")
    wx.startPullDownRefresh()
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
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getTradeNumbers',
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        var data = response.data
        console.log(data)
        this.setData({
          'weizhifu': data.weizhifu,
          'daishouhuo': data.daishouhuo,
          "yiwancheng": data.yiwancheng,
        })
        wx.stopPullDownRefresh()
      }
    })
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