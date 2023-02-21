// pages/ypdg/ypdg.js
const app = getApp();
const common = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    appointment: {
      hospital: "",
      expertName: "",
      idCard: "",
      costumerName: "",
      tel: "",
    },
  },
  testInputRule() {
    if (!this.data.appointment.hospital) {
      wx.showToast({
        title: '请输入医院',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    if (!this.data.appointment.expertName) {
      wx.showToast({
        title: '请输入专家名称',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    if (!this.data.appointment.costumerName) {
      wx.showToast({
        title: '请输入您的姓名',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    if (!this.data.appointment.idCard) {
      wx.showToast({
        title: '请输入您的身份证号码',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    var pattern = /^1\d{10}$/;
    if (!pattern.test(this.data.appointment.tel)) {
      wx.showToast({
        title: '请输入正确的电话号码',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    return true
  },
  inputDone(e) {
    var value = e.detail.value;
    var key = e.currentTarget.dataset.key;
    console.log(key)
    var appointment = this.data.appointment;
    appointment[key] = value
    this.setData({
      appointment: appointment
    })
  },
  submit(e) {
    if (!this.testInputRule()) {
      return
    }   
    this.submitAppointment()
  },
  submitAppointment() {
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/submitFormsClient',
      method: 'POST',
      data: {
        data: JSON.stringify(this.data.appointment),
        types: "专家预约"
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success(res) {
        wx.showToast({
          title: '提交成功',
          icon: 'success',
          duration: 3000
        })
      },
      fail() {
        wx.showToast({
          title: '提交失败，请稍后再试',
          icon: 'none',
          duration: 3000
        })
      },
      complete: _ => {
        console.log(this)
        var appointment = {
          hospital: "",
          expertName: "",
          idCard: "",
          costumerName: "",
          tel: "",
        }
        this.setData({
          appointment: appointment
        })
      }
    })
  },
  onLoad: function (options) {
    wx.a = this;
  },
  buyMedicine() {
    // 依次传入product_id,amount
    common.launchTrade(3, 1);
  }
})