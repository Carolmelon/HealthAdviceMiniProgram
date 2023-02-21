//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    // var logs = wx.getStorageSync('logs') || []
    // logs.unshift(Date.now())
    // wx.setStorageSync('logs', logs)

    // // 提前获取权限测试
    // wx.authorize({
    //   scope: "scope.userLocation"
    // })

    // // 打电话接口测试
    // wx.makePhoneCall({
    //   phoneNumber: "example"
    // })

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              console.log(res)
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    // url_prefix: 'http://127.0.0.1:8011',
    url_prefix: 'https://www.example.cn',
    tel: '',
    currentTrade: {
      // time: "2008-12-04 11:50",
      // amount: "2",
      // total_price: "0.02",
      // product_id: 15,
      // img: "/wx_mini/getProjectImg/1543826665543.png"
    },//time, amount, total_price, product_id, img
  }
})