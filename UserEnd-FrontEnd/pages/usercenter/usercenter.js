//index.js
//获取应用实例
const app = getApp()
const common = require('../../utils/util.js')

Page({
  data: {
    child_page: 1,
    images: [],
    imageName: "",
    name: "",
    //下面是文章列表信息（单独），上面是提交表单的信息（公用）
    pagesArray: [111, 222, 333],
    articleDatas: {
      total: 0,
      pages: 0,
      currentPage: 0,
      articles: [],
    },
    url_prefix: app.globalData.url_prefix,
  },
  onLoad: function (options) {
    wx.a = this;
    var child_page = options.page || 1;
    this.setData({
      child_page: child_page
    })
    this.gotoCertainPage(1, this.data.child_page)
  },
  test() {
    'api_test'
    var cookie = wx.getStorageSync("cookiesAndSessionId")
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/api_test/',
      data: {

      },
      header: {
        'content-type': 'application/json', // 默认值
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success(res) {
        console.log(res)
      }
    })
  },
  changeChildPage(i) {
    console.log(i.currentTarget.dataset.id)
    var id = i.currentTarget.dataset.id
    this.setData({
      child_page: id
    })
    this.gotoCertainPage(1, id)
  },
  chooseImg(e) {
    wx.chooseImage({
      sizeType: ['original', 'compressed'],  //可选择原图或压缩后的图片
      sourceType: ['album', 'camera'], //可选择性开放访问相册、相机
      count: 1, // 一次最多1张
      success: res => {
        for (var i = 0; i < res.tempFiles.length; i++) {
          var M_size = res.tempFiles[i].size / 1024 / 1024
          if (M_size > 2) {
            wx.showToast({
              title: '单个文件不能超过2M',
              icon: 'none',
              duration: 2000
            })
            return
          }
        }
        var images = res.tempFilePaths
        // 限制最多只能留下1张照片
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
  testInputRule(){
    if (!this.data.images.length) {
      wx.showToast({
        title: '请先选择图片',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    if (!this.data.name) {
      wx.showToast({
        title: '请输入姓名',
        icon: 'none',
        duration: 2000
      })
      return false
    }
    return true
  },
  submit() {
    if (!this.testInputRule()) {
      return
    }
    // 生成随机文件名
    this.data.imageName = common.randomString()
    this.setData({
      imageName: this.data.imageName
    })

    wx.showLoading({
      title: '提交中',
    })


    wx.uploadFile({
      url: app.globalData.url_prefix + '/wx_mini/uploadFileClient', //仅为示例，非真实的接口地址
      filePath: this.data.images[0],
      name: this.data.imageName,
      formData: {
        'user': 'test'
      },
      success: res => {
        console.log(this.data.imageName)
        this.submitMedicine()
        wx.hideLoading()
      },
      fail: err => {
        wx.hideLoading()
        wx.showToast({
          title: '提交失败，请稍后再试',
          icon: 'none',
          duration: 3000
        })
      }
    })
  },
  changeName(e){
    console.log(e.detail.value)
    this.setData({
      name: e.detail.value
    })
  },
  submitMedicine() {
    var data = {
      name: this.data.name,
      imageName: this.data.imageName
    }
    var types;
    if (this.data.child_page == 1)
      types = "个人档案"
    else if (this.data.child_page == 2)
      types = "专家建议"
    else 
      types = "图片资料"
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/submitFormsClient',
      method: 'POST',
      data: {
        data: JSON.stringify(data),
        types: types
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
        this.setData({
          images: [],
          imageName: "",
          name: "",
        })
      }
    })
  },
  gotoCertainPage(e, child_page_id) {
    var categoryId = Number(child_page_id) + 24
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getArticleListByOpenIdClient?categoryId=' + categoryId +'&page=' + e,
      header: {
        'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
      },
      success: response => {
        var arrays = [];
        for (var i = 1; i <= response.data.pages; i++) {
          arrays.push(i);
        }
        this.setData({
          articleDatas: response.data,
          pagesArray: arrays,
        })
      }
    })
  },
  bindPickerChange(e) {
    var index = Number(e.detail.value) + 1;
    console.log(index);
    this.gotoCertainPage(index, this.data.child_page);
  },
  previousPage() {
    if (this.data.articleDatas.currentPage <= 1)
      return
    this.gotoCertainPage(this.data.articleDatas.currentPage - 1, this.data.child_page)
  },
  nextPage() {
    if (this.data.articleDatas.currentPage >= this.data.articleDatas.pages)
      return
    this.gotoCertainPage(this.data.articleDatas.currentPage + 1, this.data.child_page)
  },
  gotoArticleDetail(e) {
    console.log(e.currentTarget.dataset)
    wx.navigateTo({
      url: '../articleDetail/articleDetail?id=' + e.currentTarget.dataset.id
    })
  },
})