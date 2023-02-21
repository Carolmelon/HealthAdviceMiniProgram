// pages/tradeList/tradeList.js
var sliderWidth = 96; // 需要设置slider的宽度，用于计算中间位置
const app = getApp()
const common = require("../../utils/util.js")

Page({
  data: {
    tabs: ["全部", "未支付", "待收货", "已完成"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
 
    pagesArray: [111, 222, 333],
    tradeDatas: {
      total: 0,
      pages: 0,
      currentPage: 0,
      trades: [],
    },
    url_prefix: app.globalData.url_prefix,
  },
  onLoad: function (options) {
    var category = options.category || 0
    this.setData({
      activeIndex: category
    })
    wx.a = this;
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
        console.log(res)
        that.setData({
          sliderLeft: (res.windowWidth / that.data.tabs.length - sliderWidth) / 2,
          sliderOffset: res.windowWidth / that.data.tabs.length * that.data.activeIndex
        });
      }
    });
    this.gotoCertainPage(1)
  },
  tabClick: function (e) {
    this.setData({
      sliderOffset: e.currentTarget.offsetLeft,
      activeIndex: e.currentTarget.id
    });
    this.gotoCertainPage(1)
  },
  gotoCertainPage(e, callback) {
    wx.request({
      // trade_status 0表示全部，1表示未支付，2表示待收货，3表示已完成
      url: app.globalData.url_prefix + '/wx_mini/getTradeListClient?trade_status=' + this.data.activeIndex + '&page=' + e,
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        console.log(response.data)
        var arrays = [];
        for (var i = 1; i <= response.data.pages; i++) {
          arrays.push(i);
        }
        this.setData({
          tradeDatas: response.data,
          pagesArray: arrays,
        })
        if(callback)
          callback()
      }
    })
  },
  bindPickerChange(e) {
    var index = Number(e.detail.value) + 1;
    console.log(index);
    this.gotoCertainPage(index);
  },
  previousPage() {
    if (this.data.tradeDatas.currentPage <= 1)
      return
    this.gotoCertainPage(this.data.tradeDatas.currentPage - 1)
  },
  nextPage() {
    if (this.data.tradeDatas.currentPage >= this.data.tradeDatas.pages)
      return
    this.gotoCertainPage(this.data.tradeDatas.currentPage + 1)
  },
  gotoTradeDetails(e){
    var trade_id = e.currentTarget.dataset.tradeId
    console.log("订单号：", trade_id)
    wx.navigateTo({
      url: '../tradeDetails/tradeDetails?trade_id=' + trade_id,
      success: function(res) {},
      fail: function(res) {},
      complete: function(res) {},
    })
  },
  deleteTrade(e){
    var trade_id = e.currentTarget.dataset.tradeId
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
              if(res.data.success){
                wx.showToast({
                  title: '删除成功',
                  icon: 'success',
                })
                this.gotoCertainPage(this.data.tradeDatas.currentPage)
              }
            },
            fail() {}
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      },
    })
  },
  payNow(e) {
    var trade_id = e.currentTarget.dataset.tradeId
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
          console.log("全局订单数据",trade_data)
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
    var trade_id = e.currentTarget.dataset.tradeId
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
                this.gotoCertainPage(this.data.tradeDatas.currentPage)
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
  remindLaunch(e) {
    var trade_id = e.currentTarget.dataset.tradeId
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
          this.gotoCertainPage(this.data.tradeDatas.currentPage)
        }
      },
      fail() { }
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
    this.gotoCertainPage(this.data.tradeDatas.currentPage || 1, _=>{
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