<template>
  <div id="zjjy">
        <div>
            <div style="height: 50px; background-color:#aaa;position:relative;padding-top:10px;border-radius:5px;">
                <b style="position:absolute;left:30px;">姓名</b>
                <b style="position:absolute;left:12%;">拍照/图片</b>
                <b style="position:absolute;left:35%;">用户id</b>
                <b style="position:absolute;left:70%;">留言时间</b>
                <b style="position:absolute;left:90%;">操作</b>
            </div>

            <div class="table" style="padding: 20px;">
                <div v-for="item in currentPageTrade" :key="item.id"
                style="height:60px;position:relative;line-height:60px;border-bottom:1.5px solid #ccc">
                <span style="position:absolute;left:10px;">{{item.name}}</span>
                <div style="position:absolute;left:11%;display:inline-block">
                    <div style="display:inline-block">
                    <a v-if="item.imageName" target="_blank" :href="HOST + item.imageName">
                        <img :src="HOST + item.imageName" alt="" height="55px;" width="55px" style="padding:1px;">
                    </a>
                    </div>
                </div>
                <span style="position:absolute;left:30%;font-size:12px;">{{item.openid}}</span>
                <span style="position:absolute;left:53%;">{{item.tel}}</span>
                <div style="position:absolute;right:48%;bottom: 3px;">

                </div>
                <span style="position:absolute;right:20%;">{{item.time}}</span>
                <div style="position:absolute;left:90%;">
                    <el-button
                        type="text"
                        size="mini"
                        @click="switchDetails(item.id)">
                        查看详情
                    </el-button>
                    <el-button
                        type="text"
                        size="mini"
                        @click="deleteMsg(item.id)">
                        删除
                    </el-button>
                </div>
                </div>
            </div>

            <div style="padding-bottom: 50px; padding-top: 50px;text-align:center;">
                <el-pagination
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-size="10"
                layout="total, prev, pager, next, jumper"
                :total="messageList.length">
                </el-pagination>
            </div>
        </div>

        <div id="ypdgDetails" style="position:fixed;left:0;right:0;bottom:0;top:0;background: rgba(0,0,0,0.7);display:none;">
            <!-- 编辑订单信息 -->
            <div
            style="width:800px;background-color:#fff;margin:150px auto;position:relative;border-radius:20px;overflow:auto;padding-bottom:20px;">
                <el-button @click="switchDetails(null)" style="position:absolute;right:10px;top:10px;" type="primary" plain>关闭</el-button>
                <div style="width:600px;padding:20px;">
                    <div style="height:40px;line-height:40px;border-bottom:1px solid #eee;">姓名：{{currentDetail.name}}</div>
                    <div style="height:40px;line-height:40px;border-bottom:1px solid #eee;">用户id：{{currentDetail.openid}}</div>
                    <div style="height:40px;line-height:40px;border-bottom:1px solid #eee;">留言时间：{{currentDetail.time}}</div>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
export default {
  name: 'zjjy',
  data() {
      return {
        messageList: [1,2,3],
        currentPage: 1,
        currentDetail: {},
      }
  },
  computed: {
    currentPageTrade() {
      return this.messageList.slice(
        (this.currentPage - 1) * 10,
        this.currentPage * 10
      );
    }
  },
  methods: {
    handleCurrentChange(page){
        this.currentPage = page;
    },
    refreshMessageList(){
      // messageList
      const loading = this.$loading({
        lock: true,
        text: '获取留言列表中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      var url = this.HOST + "/wx_mini/getClienFormLists" + 
      "?types=" + "专家建议";
      $.get(url)
      .then(response => {
        log(JSON.stringify(response))
        this.messageList = response
      })
      .catch(err => {
        log(err)
      })
      .always(() => {
        loading.close();
      })
      // articleListData
    },
    switchDetails(oid) {
        console.log(oid)
        var DetailsDiv = document.getElementById("ypdgDetails");
        if (DetailsDiv.style.display === "none") {
            DetailsDiv.style.display = "block";
            this.currentDetail = {}
            for(var i = 0; i < this.messageList.length; i++){
                if(this.messageList[i].id == oid){
                    this.currentDetail = this.messageList[i]
                    console.log(JSON.stringify(this.currentDetail))
                    break;
                }
            }
        } else {
            DetailsDiv.style.display = "none";
        }
    },
    deleteMsg(oid) {
        console.log(oid)
        this.$confirm('此操作将永久删除该留言, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            var url = this.HOST + "/wx_mini/deleteClienForm";
            $.post(url,{
                msg_id: oid
            })
            .then(response => {
                log(JSON.stringify(response))
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
                this.refreshMessageList()
            })
            .catch(err => {
                log(err)
            })
            .always(() => {

            })
        }).catch(() => {

        });
    }
  },
  mounted() {
      window.a = this;
      this.refreshMessageList()
  }
}
</script>

<style scoped>



</style>
