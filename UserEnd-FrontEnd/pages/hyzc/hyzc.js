// pages/grtj/grtj.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pagesArray: [111, 222, 333],
    productDatas: {
      total: 0,
      pages: 0,
      currentPage: 0,
      products: [],
    },
    url_prefix: app.globalData.url_prefix,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.a = this;
    this.gotoCertainPage(1);
  },

  gotoCertainPage(e) {
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getProductListClient?categoryId=7&page=' + e,
      success: response => {
        var arrays = [];
        for (var i = 1; i <= response.data.pages; i++) {
          arrays.push(i);
        }
        this.setData({
          productDatas: response.data,
          pagesArray: arrays,
        })
      }
    })
  },

  bindPickerChange(e) {
    var index = Number(e.detail.value) + 1;
    console.log(index);
    this.gotoCertainPage(index);
  },
  previousPage() {
    if (this.data.productDatas.currentPage <= 1)
      return
    this.gotoCertainPage(this.data.productDatas.currentPage - 1)
  },
  nextPage() {
    if (this.data.productDatas.currentPage >= this.data.productDatas.pages)
      return
    this.gotoCertainPage(this.data.productDatas.currentPage + 1)
  },
  gotoProductDetail(e) {
    console.log(e.currentTarget.dataset)
    wx.navigateTo({
      url: '../productDetail/productDetail?id=' + e.currentTarget.dataset.id
    })
  },
})