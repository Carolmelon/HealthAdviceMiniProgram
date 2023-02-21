<template>
  <div id="ManageArticle">
    <div class="inner-top"></div>
    <div class="inner-bottom">
      <div style="height: 50px;">
        <el-button @click="storeArticleOrder" class="button-left" type="success" icon="el-icon-check" plain>保存排序</el-button>
        <div>
          <div class="button-left" style="width: 10px; height: 40px; border-left: 3px solid #ddd"></div>
          <el-button @click="seeAllCategory" class="button-left" type="primary" plain>查看所有分类</el-button>
          <el-cascader
            @change="() => {refreshArticleList(), currentPage=1}"
            v-model="categoryArray"
            class="button-left"
            :options="options"
            change-on-select
          ></el-cascader>
          <div class="button-left" style="width: 10px; height: 40px; border-left: 3px solid #ddd"></div>
        </div>
      </div>
      <div style="height: 50px; background-color:#aaa;position:relative;padding-top:10px;">
        <b style="position:absolute;left:30px;">标题</b>
        <b style="position:absolute;right:60%;">类别</b>
        <b style="position:absolute;right:50%;">排序</b>
        <b style="position:absolute;right:30%;">发表时间</b>
        <b style="position:absolute;right:10%;">操作</b>
      </div>

      <div class="table" style="padding: 20px;">
        <div v-for="item in currentPageArticle" :key="item.id"
         style="height:40px;position:relative;padding-top:10px;border-bottom:1.5px solid #ccc">
          <span style="position:absolute;left:10px;">{{item.title}}</span>
          <span style="position:absolute;right:60%;">{{item.category_text}}</span>
          <div style="position:absolute;right:48%;bottom: 3px;">
            <el-input size="mini" style="width:70px;" v-model="item.order" placeholder="请输入内容"></el-input>
          </div>
          <span style="position:absolute;right:20%;">{{item.time}}</span>
          <div style="position:absolute;right:0;">
            <el-button
                type="text"
                size="mini"
                @click="gotoChangeArticle(item.id)">
                编辑
            </el-button>
            <el-button
                type="text"
                size="mini"
                @click="showArticle(item.id)">
                显示
            </el-button>
            <el-button
                type="text"
                size="mini"
                @click="deleteArticle(item.id)">
                删除
            </el-button>
          </div>
        </div>
      </div>

      <div style="padding-bottom: 50px; padding-top: 50px;">
        <el-pagination
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="10"
          layout="total, prev, pager, next, jumper"
          :total="articleListData.length">
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageArticle',
  data() {
      return {
        articleListData: [],
        currentPage: 1,
        options: [],
        categoryArray: [0, ]
      }
  },
  computed: {
    currentPageArticle(){
      return this.articleListData.slice( (this.currentPage-1)*10, this.currentPage*10 )
    }
  },
  methods: {
    gotoChangeArticle(id){
      log(id)
      this.$router.push({ name: 'ChangeArticle', params: { articleId: id }})
    },
    showArticle(id){
      log(id)
      this.$confirm('确认将该文章移出仓库？')
      .then(_ => {
        var url = this.HOST + "/wx_mini/showArticle";
        $.post(url,{
          id: id,
        })
        .then(response => {
          log(response)
          this.$notify({
              title: '成功',
              message: '文章移出仓库成功',
              type: 'success'
          })
          this.refreshArticleList();  // 刷新一下文章列表
        })
        .catch(err => {
            log(err)
            this.$notify.error({
                title: '错误',
                message: '文章移出仓库失败，请重试或联系管理员'
            })
        })
        done();
      })
      .catch(_ => {});
    },
    deleteArticle(id){
      log(id)
      this.$confirm('确认删除该文章？')
      .then(_ => {
        var url = this.HOST + "/wx_mini/deleteArticle";
        $.post(url,{
          id: id,
        })
        .then(response => {
          log(response)
          this.$notify({
              title: '成功',
              message: '删除该文章成功',
              type: 'success'
          })
          this.refreshArticleList();  // 刷新一下文章列表
        })
        .catch(err => {
            log(err)
            this.$notify.error({
                title: '错误',
                message: '删除该文章失败，请重试或联系管理员'
            })
        })
        done();
      })
      .catch(_ => {});
    },
    refreshArticleList(){
      // articleListData
      const loading = this.$loading({
        lock: true,
        text: '获取文章列表中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      var url = this.HOST + "/wx_mini/getArticleListData" + 
      "?category_array=" + JSON.stringify(this.categoryArray) + "&show=2";
      $.get(url)
      .then(response => {
        log(response)
        this.articleListData = JSON.parse(JSON.stringify(response));
      })
      .catch(err => {
        log(err)
      })
      .always(() => {
        loading.close();
      })
      // articleListData
    },
    storeArticleOrder(){
      const loading = this.$loading({
        lock: true,
        text: '保存文章排序中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      var url = this.HOST + "/wx_mini/storeArticleOrder";
      $.post(url,{
        data: JSON.stringify(this.articleListData),
      })
      .then(response => {
        log(response)
        this.$notify({
            title: '成功',
            message: '保存排序成功',
            type: 'success'
        })
        this.refreshArticleList();  // 刷新一下文章列表
      })
      .catch(err => {
        log(err)
        this.$notify.error({
            title: '错误',
            message: '保存排序失败，请重试或联系管理员'
        })
      })
      .always(() => {
        loading.close();
      })
    },
    handleCurrentChange(page){
      this.currentPage = page;
    },
    seeAllCategory(){
      this.categoryArray = [0, ]
      this.refreshArticleList()
    }
  },
  mounted() {
    this.refreshArticleList()

    //初始化分类
    var url = this.HOST + "/wx_mini/getClassifyArticle";
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
    window.a = this;
  }
}
</script>

<style scoped>

#ManageArticle {
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
}

.button-left {
  float: left;
  margin: 5px;
}

</style>
