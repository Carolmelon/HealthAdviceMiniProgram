// pages/cashierDesk/cashierDesk.js
const app = getApp();

Page({
  data: {
    tradeData: {},
    url_prefix: app.globalData.url_prefix,
    trade_id: ""
  },
  onLoad: function (options) {
    var trade_id = options.trade_id // 订单号
    this.setData({
      trade_id: trade_id
    })
    console.log(trade_id)
    wx.a = this;
    var tradeData = app.globalData.currentTrade // 当前交易信息
    this.setData({
      tradeData: tradeData
    })

    if (JSON.stringify(this.tradeData) === "{}") {
      // 非法进入
      setTimeout(_ => {
        wx.redirectTo({
          url: '../index/index',
        })
      }, 100)
    }
  },
  payMoney(){
    wx.showLoading({
      title: '加载中',
      mask: true
    })
    var data = {
      trade_id: this.data.trade_id
    }
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/payMoney',
      method: 'POST',
      data: {
        data: JSON.stringify(data)
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        wx.hideLoading()
        console.log(response.data)
        var data = response.data
        if (data.err_code == 1){
          wx.showToast({
            title: data.msg_data,
            icon: 'none',
            duration: 5000,
            success: function(res) {},
            fail: function(res) {},
            complete: function(res) {},
          })
        }
        if (data.success === true){
          wx.requestPayment({
            timeStamp: data.timeStamp,
            nonceStr: data.nonceStr,
            package: data.package,
            signType: "MD5",
            paySign: data.paySign,
            'success': res=> {
              var data = {
                trade_id: this.data.trade_id
              }
              wx.request({
                url: app.globalData.url_prefix + '/wx_mini/paySuccess',
                method: 'POST',
                data: {
                  data: JSON.stringify(data)
                },
                header: {
                  'content-type': 'application/x-www-form-urlencoded', // 默认值
                  'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
                },
                success: res => {
                  wx.showToast({
                    title: "支付成功",
                    icon: 'success',
                    duration: 1500,
                    success: function (res) { },
                    fail: function (res) { },
                    complete: function (res) { },
                  })
                },
                complete: _=> {
                  setTimeout(_=>{
                    wx.reLaunch({
                      url: '../trueUserCenter/trueUserCenter',
                      success: function (res) { },
                      fail: function (res) { },
                      complete: function (res) { },
                    })
                  }, 1500)
                }
              })
            },
            'fail': function (res) {
              console.log(res)
            },
            'complete': function (res) {
              console.log(res)
            }
          })
        }
      }
    })
  }
})