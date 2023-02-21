// pages/tradeDetails/tradeDetails.js
const app = getApp();
const common = require("../../utils/util.js")

Page({
 
  /**
   * 页面的初始数据
   */
  data: {
    trade_data: {
      // trade_id: "20181205030420942869",
      // order_time: "2018-12-5 22:27:18",
      // pay_time: "2018-12-5 22:36:25",
      // trade_status: 2,
      // trade_status_text: "待收货",
      // total_price: "0.02", //实付款
      // tel: "example", // 电话
      // liuyan: "搞快点，臭弟弟。搞快点，臭弟弟。搞快点，臭弟弟。搞快点，臭弟弟。搞快点，臭弟弟。搞快点，臭弟弟。搞快点，臭弟弟。", // 留言备注
      // product_id: "51",
      // product_img: "/wx_mini/getProjectImg/1543949209560.png",
      // product_name: "1分钱的东西1分钱的东西1分钱的东西1分钱的东西",
      // amount: "2",
      // product_price: "0.01",
    },
    url_prefix: app.globalData.url_prefix,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("加载")
    '20181205030420942869'
    var trade_id = options.trade_id || '20181205030420942869'
    console.log("订单详情页：" + trade_id)
    wx.showLoading({
      title: '获取订单详情中',
    })
    this.getTradeDetailsByIdClient(trade_id, _=>{
      wx.hideLoading();
    })
  },
  gotoProductDetails(){
    wx.navigateTo({
      url: '../productDetail/productDetail?id=' 
      + this.data.trade_data.product_id,
    })
  },
  getTradeDetailsByIdClient(trade_id, success){
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getTradeDetailsByIdClient?trade_id=' + trade_id,
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        console.log(response)
        this.setData({
          trade_data: response.data,
        })
        success()
      }
    })
  },
  deleteTrade(e) {
    var trade_id = this.data.trade_data.trade_id
    console.log("订单号：", trade_id)
    wx.showModal({
      title: '提示',
      content: '确定删除该订单吗？',
      success: res => {
        if (res.confirm) {
          wx.request({
            url: app.globalData.url_prefix + '/wx_mini/deleteTradeClient?trade_id='
              + trade_id,
            method: 'GET',
            header: {
              'content-type': 'application/x-www-form-urlencoded', // 默认值
              'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
            },
            success: res => {
              if (res.data.success) {
                wx.showToast({
                  title: '删除成功',
                  icon: 'success',
                })
                wx.navigateBack({
                  delta: 1
                })
              }
            },
            fail() { }
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      },
    })
  },
  payNow(e) {
    var trade_id = this.data.trade_data.trade_id
    console.log("订单号：", trade_id)
    // 下面这段是把trade的信息放到，写些什么垃圾代码
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getTradeDetailsByIdClient?trade_id=' + trade_id,
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: res => {
        console.log(res.data);
        if (res.data.trade_status != 1) {
          wx.showToast({
            title: '该订单不可支付',
            icon: 'none',
            image: '',
            duration: 2000,
            mask: true
          })
        }
        else {
          var data = res.data;
          // time: "2008-12-04 11:50",
          // amount: "2",
          // total_price: "0.02",
          // product_id: 15,
          // img: "/wx_mini/getProjectImg/1543826665543.png"
          var trade_data = {
            img: data.product_img,
            time: data.order_time,
            amount: data.amount,
            total_price: data.total_price,
            product_id: data.product_id
          }
          console.log("全局订单数据", trade_data)
          app.globalData.currentTrade = trade_data
          wx.navigateTo({
            url: '../cashierDesk/cashierDesk?trade_id=' + trade_id,
          })
        }
      },
      fail() {
        wx.showToast({
          title: '进入支付失败，请稍后再试',
          icon: 'none',
          duration: 3000
        })
      }
    })
  },
  sureTrade(e) {
    var trade_id = this.data.trade_data.trade_id
    console.log("订单号：", trade_id)
    wx.showModal({
      title: '提示',
      content: '确定已经收货吗？',
      success: res => {
        if (res.confirm) {
          wx.request({
            url: app.globalData.url_prefix + '/wx_mini/sureTradeClient?trade_id='
              + trade_id,
            method: 'GET',
            header: {
              'content-type': 'application/x-www-form-urlencoded', // 默认值
              'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
            },
            success: res => {
              if (res.data.success) {
                wx.showToast({
                  title: '确认成功',
                  icon: 'success',
                })
                wx.startPullDownRefresh()
              }
            },
            fail() { }
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      },
    })
  },
  call_telephone(){
    wx.showModal({
      title: "提示",
      content: '确认咨询卓越壹生吗？',
      success(res) {
        if (res.confirm) {
          wx.makePhoneCall({
            phoneNumber: "15884176782",
          })
        } else if (res.cancel) {
          
        }
      }
    })
  },
  remindLaunch(e) {
    var trade_id = this.data.trade_data.trade_id
    console.log("订单号：", trade_id)
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/remindUs?trade_id='
        + trade_id,
      method: 'GET',
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: res => {
        if (res.data.success) {
          wx.showToast({
            title: '提醒成功',
            icon: 'success',
          })
        }
      },
      fail() {}
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
    console.log("显示")
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
    this.getTradeDetailsByIdClient(this.data.trade_data.trade_id, _=>{
      wx.stopPullDownRefresh()
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