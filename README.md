# 项目背景

大三上（2018年10月）的某一天，一个朋友叫我帮他做一个微信小程序，内容是医疗服务相关的，然后针对他的想法提了一些具体的需求，于是就产生了这个小小的project。之前虽然写过一些前端代码，主要涉及的是Vue.js，没接触过微信小程序，但本着MVVC结构的前端框架都差不多的想法，就花了7天左右的时间写了这个项目，是为了快速给出一个可用的版本。最后由于他们公司没有医疗相关的资格证书，我们这个微信小程序没有审核通过，也就没有花时间去重构，所以里面一些前端代码写得有一点点乱，比如微信小程序的很多前端样式直接写在DOM里面：

```html
<view style="text-align:center;margin-top:0px;margin-bottom:0px;padding:0px;color:#5A5A5A;font-family:&quot;font-size:16px;white-space:normal;">
```

比较不符合开发的规范，当时写的时候就意识到这个问题，但是时间比较紧，前后端都需要一个人写，想着一个人写就不用太注意代码规范了，反正自己能看懂就行（其实是不对的）。由于小程序最终没上线，也没有花时间去重构，但是功能实现得还是很多的。

# 简介

- 一个相对完善的商城&咨询微信小程序。接入了微信支付，管理系统中集成了富文本编辑器，可以让不懂前端的运营也能通过简单的排版工具（秀米等）添加内容。
- 采用MVVC结构的前后端分离开发，界面比较丝滑。

# 结构

<img src="Illustrations\architecture.png" alt="image-20230222031759416" style="zoom:60%;" />

这个项目大概就是上图所示的三个部分组成，这三个部分和<a href="#dir-struct">目录结构</a>中的三个部分对应。它们分别是：

- UserEnd-FrontEnd	——用户端前端
- ManagementSystem-FrontEnd	——管理系统前端
- ALL-Backend	——后端

# 演示

- 小程序**用户端**的一个演示视频，<a href='Illustrations/小程序用户端＋邮件提醒.mp4'>点击</a>跳转到演示视频

<video src='Illustrations/小程序用户端＋邮件提醒.mp4' width='30%'></video>


- 小程序**管理端**的一个演示视频，<a href='Illustrations/小程序管理端.mp4'>点击</a>跳转到演示视频

<video src='Illustrations/小程序管理端.mp4' width='90%'></video>



# <span id="dir-struct">目录结构</span>

- ALL-Backend								后端，使用Django框架
  - app1										一些具体的处理请求的逻辑都在里面
  - static										静态的资源文件
  - templates								登录界面的前端MVC模板，整个项目除了这里的少量界面采用MVC，其他都是前后端分离的MVVC模式
  - ......
- UserEnd-FrontEnd							用户端，前端界面，使用微信小程序的那套语言，对应上面第一个演示视频
  - utils/util.js									定义了一些通用的函数，比如发起订单
  - pages											一些模块，每一个模块对应小程序的一个具体的MVVC界面
    - index
    - tradeDetails
    - aboutUs
    - articleDetail
    - usercenter
    - productDetail
    - ......
  - wxParse											小程序富文本解析的一个库，用于将我们在管理系统中保存的商品/文章富文本信息，形式为带有图片和排版格式HTML（我在管理系统中内置了一个kindEditor，可以将秀米等工具排版后的内容直接粘贴到里面存到数据库里，然后以HTML形式存到数据库里），转换为wxml兼容的形式。此库的详细信息：https://github.com/icindy/wxParse
  - app.js
  - app.json
  - app.wxss
  - ......
- ManagementSystem-FrontEnd					管理系统，前端界面，使用Vue.js，对应上面第二个演示视频
  - build
  - config
  - dist															vue最终编译出来的静态文件所在的文件夹
  - src
    - pages													一些Vue.js的MVVC界面，一个界面对应一个文件/文件夹
      - Articles											文章详情页，里面含有一个富文本编辑器kindEditor，可以直接保存秀米等排版工具粘贴过来的内容，转换成HTML保存到数据库中。
      - Products											商品详情页
      - messages
      - Index.vue											首页
      - TradeManage.vue
      - ......
    - router/index.js												Vue.js的路由，定义url和界面的对应关系
    - store/index.js													其中定义了一些全局的状态变量，这些变量可以跨界面而不改变
    - components													一些通用的模块，会被多个界面所引用
      - Asides.vue												边栏
      - ChangeArticle.vue									修改文章
      - ChangeProduct.vue								修改商品
    - App.vue
    - main.js
    - ......
  - static
  - .babelrc
  - index.html
  - ......

​		

# 计划

- 重新把程序跑起来。之前租的腾讯云服务器和域名都过期了，但微信小程序需要HTTPS和域名（不能用ip），所以要run起来还要费点精力。
- 重构代码，加点注释。
