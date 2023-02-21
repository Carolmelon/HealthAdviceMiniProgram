<template>
  <div id="app" style="min-width:1300px;">
    <el-row class="rowInApp">

      <el-col class="colInApp" :span="5">
        <div class="asidesInApp">
          <Asides />
        </div>
      </el-col>

      <el-col class="colInApp" style="min-width:1000px;" :span="19">
        <div class="routerViewInApp">
          <router-view/> <!-- 路由入口 -->
        </div>
      </el-col>
      
    </el-row>

  </div>
</template>

<script>
window.log = console.log.bind(console);

import Asides from "./components/Asides";

export default {
  name: "App",
  data() {
    return {};
  },
  components: {
    Asides
  },
  mounted() {
    var appendArticlesOptions = {
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
      var appendArticleContent = K.create("#appendArticleContent", appendArticlesOptions);
      window.appendArticleContent = appendArticleContent;
    });
  },
  created(){
    window.alert = argument => {
      this.$notify.error({
        title: '错误',
        message: argument
      })
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #858585;
  font-size: 14px;
  height: 100%;
}

html, body, .rowInApp, .colInApp {
  height: 100%;
}

body {
  background-color: #eeeeee;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.asidesInApp { /* 左侧边栏 */
  min-height: 50px;
  background-color: slategray;
  height: 100%;
  border-bottom-right-radius: 200px;
  border-bottom-left-radius: 200px;
}

.routerViewInApp {  /* 右边正文 */
  min-height: 50px;
  height: 100%;
  /* opacity: 0.8; */
}

b {
  color: white;
}

</style>
