// pages/comfirmTrade/comfirmTrade.js
const app = getApp();
const common = require("../../utils/util.js")

Page({

  /**
   * 页面的初始数据
   */
  data: {
    tradeData: {},
    url_prefix: app.globalData.url_prefix,
    liuyan: ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.a = this;
    var tradeData = app.globalData.currentTrade
    this.setData({
      tradeData: tradeData
    })

    if (JSON.stringify(this.tradeData) === "{}"){
      // 非法进入
      setTimeout(_=>{
        wx.redirectTo({
          url: '../index/index',
        })
      }, 100)
    }

    console.log(tradeData)

  },
  changeliuyan(e){
    this.setData({
      liuyan: e.detail.value
    })
  },

  trueLaunchTrade(){
    'trueLaunchOrder'
    var data = this.data.tradeData;
    data.liuyan = this.data.liuyan;
    console.log(data)
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/trueLaunchOrder',
      method: 'POST',
      data: {
        data: JSON.stringify(data)
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        console.log(response.data)
        if(response.data.success != true){
          wx.showToast({
            title: '提交订单失败，请稍后再试',
            icon: 'none',
            duration: 3000
          })
        }else{
          wx.navigateTo({
            url: '../cashierDesk/cashierDesk?trade_id=' + response.data.trade_id,
          })
        }
      }
    })
  },

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