// pages/ypdg/ypdg.js
const app = getApp();
const common = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    medicine:{
      name: "",
      tel: "",
      changjia: "",
      guige: "",
      amount: "",
      hospital: "",
      imageNames: [],
    },
    images: [],
  },
  testInputRule(){
    if(!this.data.medicine.name){
      wx.showToast({
        title: '请输入药品名',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    var pattern = /^1\d{10}$/;
    if(!pattern.test(this.data.medicine.tel)){
      wx.showToast({
        title: '请输入正确的电话号码',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    return true
  },
  inputDone(e){
    var value = e.detail.value;
    var key = e.currentTarget.dataset.key;
    console.log(key)
    var medicine = this.data.medicine;
    medicine[key] = value
    this.setData({
      medicine: medicine
    })
  },
  chooseImg(e){
    wx.chooseImage({
      sizeType: ['original', 'compressed'],  //可选择原图或压缩后的图片
      sourceType: ['album', 'camera'], //可选择性开放访问相册、相机
      count: 3, // 一次最多3张
      success: res => {
        for (var i = 0; i < res.tempFiles.length; i++){
          var M_size = res.tempFiles[i].size / 1024 / 1024
          if(M_size > 2){
            wx.showToast({
              title: '单个文件不能超过2M',
              icon: 'none',
              duration: 2000
            })
            return
          }
        }
        var images = this.data.images
        images = images.concat(res.tempFilePaths)
        // 限制最多只能留下3张照片
        images = images.length <= 3 ? images : images.slice(0, 3)
        this.setData({
          images: images
        })
      }
    })
  },
  removeImage(e) {
    const idx = e.target.dataset.idx
    this.data.images.splice(idx, 1)
    this.setData({
      images: this.data.images
    })
  },
  handleImagePreview(e) {
    const idx = e.target.dataset.idx
    const images = this.data.images
    wx.previewImage({
      current: images[idx],  //当前预览的图片
      urls: images,  //所有要预览的图片
    })
  },
  submit(e){
    if (!this.testInputRule()){
      return
    }

    var img_number = this.data.images.length;
    // 生成随机文件名,先清空,再填充
    this.data.medicine.imageNames = []
    this.setData({
      medicine: this.data.medicine
    })
    for(var i = 0; i < img_number; i++){
      this.data.medicine.imageNames.push(common.randomString())
    }
    this.setData({
      medicine: this.data.medicine
    })

    console.log(this.data.medicine.imageNames)

    wx.showLoading({
      title: '提交中',
    })

    var all_uploaded_img_amount = 0;

    for(var i = 0; i < img_number; i++){
      wx.uploadFile({
        url: app.globalData.url_prefix + '/wx_mini/uploadFileClient', //仅为示例，非真实的接口地址
        filePath: this.data.images[i],
        name: this.data.medicine.imageNames[i],
        formData: {
          'user': 'test'
        },
        success: res => {
          var that = this;
          all_uploaded_img_amount += 1;
          if (all_uploaded_img_amount == img_number){
            // 所有文件上传完毕
            wx.hideLoading()
            this.submitMedicine()
          }
        },
        fail: err=>{
          wx.hideLoading()
          wx.showToast({
            title: '提交失败，请稍后再试',
            icon: 'none',
            duration: 3000
          })
        }
      })
    }

    if (!img_number)
      this.submitMedicine()
  },
  submitMedicine(){
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/submitFormsClient',
      method: 'POST',
      data: {
        data: JSON.stringify(this.data.medicine),
        types: "药品代购"
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
      fail(){
        wx.showToast({
          title: '提交失败，请稍后再试',
          icon: 'none',
          duration: 3000
        })
      },
      complete: _ => {
        console.log(this)
        var data = {
          medicine: {
            name: "",
            tel: "",
            changjia: "",
            guige: "",
            amount: "",
            hospital: "",
            imageNames: [],
          },
          images: [],
        }
        this.setData({
          medicine: data.medicine,
          images: data.images
        })
      }
    })
  },
  onLoad: function (options) {
    wx.a = this;
  },
  buyMedicine(){
    // 依次传入product_id,amount
    common.launchTrade(2, 1);
  }
})