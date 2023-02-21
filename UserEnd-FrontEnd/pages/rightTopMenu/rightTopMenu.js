// pages/rightTopMenu/rightTopMenu.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    value: 0,
    menusArray: [ 
    "关于我们",  //0
    "视频咨询", "个人体检", 
    "团购体检", "健康指南", 
    "专家预约", "药品代购", 
    "会员套餐", "家庭健康管理组"
    ]
  },

  /**
   * 组件的方法列表
   */
  methods: {
    bindPickerChange(e){
      console.log(e.detail)
      var index = e.detail.value
      if(index == "0")
        wx.navigateTo({
          url: '../aboutUs/aboutUs',
        })
      if(index == "1")
        wx.navigateTo({
          url: '../videoQuery/videoQuery',
        })
      if (index == "2")
        wx.navigateTo({
          url: '../grtj/grtj',
        })
      if (index == "3")
        wx.navigateTo({
          url: '../tgtj/tgtj',
        })
      if (index == "4")
        wx.navigateTo({
          url: '../jkzn/jkzn',
        })
      if (index == "5")
        wx.navigateTo({
          url: "../zjyy/zjyy",
        })
      if (index == "6")
        wx.navigateTo({
          url: '../ypdg/ypdg',
        })
      if (index == "7")
        wx.navigateTo({
          url: '../hyzc/hyzc',
        })
      if (index == "8")
        wx.navigateTo({
          url: '../homeHealthManage/homeHealthManage',
        })
    }
  }
})
