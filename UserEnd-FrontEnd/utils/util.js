const app = getApp();

const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

function randomString(len) {
　　len = len || 32;
　　var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
　　var maxPos = $chars.length;
　　var pwd = '';
　　for (var i = 0; i < len; i++) {
  　　　　pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
　　}
　　return pwd;
}

function launchTrade(product_id, amount){
  var req_data = {
    product_id: product_id,
    amount: amount
  }
  wx.request({
    url: app.globalData.url_prefix + '/wx_mini/launchOrder',
    method: 'POST',
    data: {
      data: JSON.stringify(req_data)
    },
    header: {
      'content-type': 'application/x-www-form-urlencoded', // 默认值
      'cookie': wx.getStorageSync("cookiesAndSessionId")  // 使用之前存入的cookie
    },
    success(res) {
      console.log(res.data);
      if(res.data.error_code === 1){
        wx.showModal({
          title: '提示',
          content: '当前账户没有设置手机号，是否立即设置？',
          success(res) {
            if (res.confirm) {
              wx.navigateTo({
                url: '../setTel/setTel',
              })
            } else if (res.cancel) {
              console.log('用户点击取消')
            }
          }
        })
      }
      else if (res.statusCode != 200){
        wx.showToast({
          title: '提交订单失败，请稍后再试',
          icon: 'none',
          duration: 3000
        })
      }
      else {
        console.log(res)
        app.globalData.currentTrade = res.data
        wx.navigateTo({
          url: '../comfirmTrade/comfirmTrade',
        })
      }
    },
    fail() {
      wx.showToast({
        title: '提交订单失败，请稍后再试',
        icon: 'none',
        duration: 3000
      })
    }
  })
}

function checkTel(fail){
  var tel = app.globalData.tel
  if(!tel){
    wx.showModal({
      title: '提示',
      content: '当前没有绑定手机号，是否立即绑定？',
      success(res) {
        if (res.confirm) {
          wx.navigateTo({
            url: '../setTel/setTel',
          })
        } else if (res.cancel) {
          wx.navigateBack({
            delta: 1
          })
        }
      }
    })
  }
}

function remindUs(trade_id){
  console.log(trade_id)
}

function sureOrder(trade_id) {
  console.log(trade_id)
}

function deleteOrder(trade_id) {
  console.log(trade_id)
}

module.exports = {
  formatTime: formatTime,
  randomString: randomString,
  launchTrade: launchTrade,
  checkTel: checkTel,
  remindUs: remindUs,
  sureOrder: sureOrder,
  deleteOrder: deleteOrder,
}
