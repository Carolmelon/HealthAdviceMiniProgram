// pages/articleDetail/articleDetail.js
const app = getApp();
const WxParse = require('../../wxParse/wxParse.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    article: false,
    url_prefix: app.globalData.url_prefix,
    wxml: null,
    show_img: false, // 是否显示文章缩略图
    center: false, // 是否居中显示摘要
    show_banner: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var show_img = options.show_img;
    var center = options.center;
    console.log("哈哈: " ,show_img, center)
    if(show_img && center)
      this.setData({
        show_img: show_img,
        center: center
      })
    wx.showLoading({
      title: '加载中',
    })
    var id = options.id || 103
    'getArticleByIdClient'
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getArticleByIdClient?id=' + id,
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        // console.log(response)
        this.setData({
          article: response.data,
        })
        wx.hideLoading()
        WxParse.wxParse("wxml", "html", response.data.content, this)
      }
    })

    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getOpenOrNot',
      success: response => {
        if (response.data == true)
          this.setData({
            show_banner: true
          })
      }
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