<template>
  <div id="AppendArticle">
    <!-- <div class="inner-top">添加产品</div> -->
    <div class="inner-bottom">

      <div class="row">
        <span class="title">产品名称*</span>
        <el-input class="input" v-model="articleData.name" placeholder="请输入内容"></el-input>
      </div>

      <div class="row">
        <span class="title">选择分类</span>
        <el-cascader
        class="input"
        placeholder=""
        :options="options"
        filterable
        change-on-select
        v-model="articleData.category"
      ></el-cascader>
      </div>
      
      <!-- <div class="row">
        <span class="title">文章作者</span>
        <el-input class="input" v-model="articleData.author" placeholder="请输入内容"></el-input>
      </div> -->

      <div class="row">
        <span class="title">发布时间</span>
        <el-input class="input" v-model="articleData.time" placeholder="请输入内容"></el-input>
      </div>

      <div class="row" style="height: 100px;">
        <span class="title">产品图</span>
        <img id="thumbnail-preview" 
        style=" border: 1px solid black; " alt="无图片" />
        <input id="thumbnail" type="file" style="display: none">
        <el-button type="primary" plain @click="selectFile"
        style="position: absolute; left: 250px; bottom: 10px;">选择图片</el-button>
      </div>

      <div class="row">
        <span class="title">产品状态</span>
        <div class="row-right-div" style="top: 14px;">
          <el-radio v-model="articleData.productStatus" label="1">立即发布</el-radio>
          <el-radio v-model="articleData.productStatus" label="2">放入仓库</el-radio>
        </div>
      </div>

      <div class="row">
        <span class="title">市场价</span>
        <el-input class="input" v-model="articleData.originPrice" placeholder="请输入内容"></el-input>
      </div>

      <div class="row">
        <span class="title">价格</span>
        <el-input class="input" v-model="articleData.price" placeholder="请输入内容"></el-input>
      </div>

      <div class="row">
        <span class="title">产品摘要</span>
        <el-input type="textarea" :row="4" class="input" v-model="articleData.digest" placeholder="请输入内容"></el-input>
      </div>

      <div class="row" style="margin-top: 30px;">
        <span class="title">详细内容*</span>
        <div style="float:right;;margin-bottom:30px;width:90%;">
        <textarea
        style="width:80%;height:300px;visibility:hidden;"
        id="appendArticleContent" 
        name="appendArticleContent"
        cols="30" 
        rows="10">
        </textarea></div>
      </div>
      
      <div style="clear:both;"></div>

      <div style="">
        <el-button @click="uploadProduct" type="primary" plain>确定</el-button>
        <el-button @click="$router.push('/')" type="warning" plain>取消</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppendArticle",
  data() {
    return {
      // 难得改名了，凑合这个用吧
      articleData: {
        name: "", 
        category: [1], // 分类
        time: "",
        img: "",
        productStatus: "1", // 立即发布1 或者放入仓库2
        originPrice: "0.00",
        price: "0.00",
        digest: "",
        content: "",
      },
      options: [],
    };
  },
  computed: {},
  methods: {
    selectFile() {
      document.querySelector("#thumbnail").click();
    },
    bindInputTag() {
      var self = this;
      var fileInput = document.querySelector("#thumbnail");
      var preview = document.querySelector("#thumbnail-preview");
      // 监听input标签的变化
      fileInput.addEventListener("change", function() {
        // 清除背景图片:
        preview.src = "";
        // 检查文件是否选择:
        if (!fileInput.value) {
          return;
        }
        // 获取File引用:
        var file = fileInput.files[0];
        // 获取File信息:
        // info.innerHTML =
        //   "文件: " +
        //   file.name +
        //   "<br>" +
        //   "大小: " +
        //   file.size +
        //   "<br>" +
        //   "修改: " +
        //   file.lastModifiedDate;
        if (file.size > 2097152) {
          fileInput.value = null;
          alert("文件不能超过2MB");
          return;
        }
        if (
          file.type !== "image/jpeg" &&
          file.type !== "image/png" &&
          file.type !== "image/gif"
        ) {
          fileInput.value = null;
          alert("不是有效的图片文件!");
          return;
        }
        // 读取文件:
        var reader = new FileReader();
        reader.onload = function(e) {
          var data = e.target.result; // 'data:image/jpeg;base64,/9j/4AAQSk...(base64编码)...'
          preview.src = data;
          self.articleData.img = data; // data里面的img信息
        };
        // 以DataURL的形式读取文件:
        reader.readAsDataURL(file);
      });
    },
    uploadProduct() {
      this.articleData.content = window.appendArticleContent.html()
      // log(this.articleData)
      if(!Boolean(this.articleData.name)){
        this.$notify.error({
          title: '错误',
          message: '没有产品名'
        })
        return;
      }
      if(!Boolean(this.articleData.content)){
        this.$notify.error({
          title: '错误',
          message: '没有详细内容'
        })
        return;
      }
      //打开等待框
      const loading = this.$loading({
        lock: true,
        text: '添加产品中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      var url = this.HOST + "/wx_mini/uploadProduct";
      $.post(url,{
        productData: JSON.stringify(this.articleData),
      })
      .then(response => {
        log(response)
        this.$notify({
          title: '成功',
          message: '添加产品成功',
          type: 'success'
        })
      })
      .catch(err => {
        log(err)
        this.$notify.error({
          title: '错误',
          message: '添加产品失败，请重试或联系管理员'
        })
      })
      .always(() => {
        loading.close();
      })
    }
  },
  mounted() {
    // 初始化articleData里面的一些信息
      //初始化时间
    var d = new Date();
    this.articleData.time = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate() + " " + d.toLocaleTimeString()
      //初始化分类
    var url = this.HOST + "/wx_mini/getClassifyProduct";
    $.get(url)
    .then(response => {
      log(response)
      this.options = JSON.parse(JSON.stringify(response));
    })
    .catch(err => {
      log(err)
    })
    .always(() => {
      
    })

    // 绑定缩略图上传即显示
    this.bindInputTag(); 
    // 注册kindeditor
    var options = {
      cssPath: "/static/kindeditor/plugins/code/prettify.css",
      uploadJson: this.HOST + "/wx_mini/uploadFile",
      //fileManagerJson : '/static/kindeditor/php/file_manager_json.php',
      allowFileManager: false,
      urlType: "domain",
      resizeType: 1, // 1表示只能调整高度
      width: "100%",
      allowFlashUpload: false,
      filterMode: false, //标签过滤：默认过滤不安全的标签
      allowFileUpload: false,
    };

    KindEditor.ready(function(K) {
      var appendArticleContent = K.create("#appendArticleContent", options);
      window.appendArticleContent = appendArticleContent;
    });
  },
  created(){
    window.a = this;
  },
  updated(){
  }
};
</script>

<style scoped>
#AppendArticle {
  position: relative;
  height: 100%;
}

.inner-top {
  position: absolute;
  top: 10px;
  left: 20px;
  right: 20px;
  height: 60px;
}

.inner-bottom {
  position: absolute;
  background-color: #fff;
  top: 100px;
  bottom: 20px;
  left: 20px;
  right: 20px;
  box-shadow: 0px 0px 2px 3px #e5e5e5;
  border-radius: 5px;
  overflow: auto;
  padding-bottom: 30px;
}

.row {
  position: relative;
  width: 90%;
  min-height: 50px;
  margin: 0 auto;
}

.row:first-child {
  margin-top: 30px;
}

.title {
  position: absolute;
  bottom: 18px;
  left: 5px;
}

.row-right-div {
  position: absolute;
  left: 100px;
  bottom: 0;
}

.input {
  position: absolute;
  margin-left: 50px;
  background-color: #ddd;
  width: 90%;
  left: 50px;
  right: 20px;
}

#thumbnail-preview {
  position: absolute;
  left: 100px;
  width: 100px;
  height: 100px;
}
</style>
