// pages/jkzn/jkzn.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    pagesArray: [111, 222, 333],
    articleDatas: {
      total: 0,
      pages: 0,
      currentPage: 0,
      articles: [],
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

  bindPickerChange(e) {
    var index = Number(e.detail.value) + 1;
    console.log(index);
    this.gotoCertainPage(index);
  },

  gotoCertainPage(e) {
    wx.request({
      url: app.globalData.url_prefix + '/wx_mini/getArticleListClient?categoryId=28&page=' + e,
      success: response => {
        var arrays = [];
        for (var i = 1; i <= response.data.pages; i++) {
          arrays.push(i);
        }
        var articles = response.data.articles;
        for (var i = 0; i < articles.length; i++){
          articles[i].digest = articles[i].digest.substr(0, articles[i].digest.length - 6)
        }
        this.setData({
          articleDatas: response.data,
          pagesArray: arrays,
        })
      }
    })
  },
  previousPage() {
    if (this.data.articleDatas.currentPage <= 1)
      return
    this.gotoCertainPage(this.data.articleDatas.currentPage - 1)
  },
  nextPage() {
    if (this.data.articleDatas.currentPage >= this.data.articleDatas.pages)
      return
    this.gotoCertainPage(this.data.articleDatas.currentPage + 1)
  },
  gotoArticleDetail(e) {
    console.log(e.currentTarget.dataset)
    wx.navigateTo({
      url: '../articleDetail/articleDetail?id=' + e.currentTarget.dataset.id + "&show_img=" + "true" + 
      "&center=" + "center"
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