// pages/phoneCall/phoneCall.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    wx.showModal({
      title: "提示",
      content: '确认咨询卓越壹生吗？',
      success(res) {
        if (res.confirm) {
          wx.makePhoneCall({
            phoneNumber: "15884176782",
            complete() {
              wx.switchTab({
                url: '../index/index'
              })
            }
          })
        } else if (res.cancel) {
          wx.switchTab({
            url: '../index/index'
          })
        }
      }
    })


  }

})