// pages/setTel/setTel.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    tel: "",
    newTel: "",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(app)
    this.data.tel = app.globalData.tel
    this.setData({
      tel: this.data.tel
    })
  },
  inputDone(e){
    var value = e.detail.value;
    this.setData({
      newTel: value
    })
  },
  changeTel(){
    console.log(this.data.newTel)
    var pattern = /^1\d{10}$/;
    if (!pattern.test(this.data.newTel)) {
      wx.showToast({
        title: '请输入正确的电话号码',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/changeTel',
      method: 'POST',
      data: {
        data: this.data.newTel,
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: res => {
        console.log(res.data)
        if(res.data == "ok"){
          wx.showToast({
            title: '修改成功',
            icon: 'success',
            duration: 3000
          })
          app.globalData.tel = this.data.newTel
        }
        else
          wx.showToast({
            title: '修改失败，请稍后再试',
            icon: 'none',
            duration: 3000
          })
        setTimeout(_=>{
          wx.navigateBack({
            delta: 1
          })
        }, 1000)
      },
      fail() {
        
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