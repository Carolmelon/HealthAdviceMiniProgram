<template>
  <div id="MemberManage">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        <div style="height: 50px; background-color:#aaa;position:relative;padding-top:10px;border-radius:5px;">
            <b style="position:absolute;left:10%;line-height:30px;">ID</b>
            <b style="position:absolute;left:40%;line-height:30px;">用户id</b>
            <b style="position:absolute;left:70%;line-height:30px;">电话号码</b>
        </div>
        <div style="height:20px;"></div>
        <div style="border-bottom:1px solid #eee; height:40px; width:95%;margin: 0 auto;" v-for="item in currentPageList" :key="item.id">
            <span style="position:absolute;left:10%;line-height:40px;">{{item.id}}</span>
            <span style="position:absolute;left:40%;line-height:40px;">{{item.openid}}</span>
            <span style="position:absolute;left:70%;line-height:40px;">{{item.tel}}</span>
        </div>
        <div style="padding-bottom: 50px; padding-top: 50px;text-align:center;">
            <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="10"
            layout="total, prev, pager, next, jumper"
            :total="memberList.length">
            </el-pagination>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MemberManage',
  data() {
      return {
        memberList: [1,2,3],
        currentPage: 1,
      }
  },
  computed: {
    currentPageList() {
      return this.memberList.slice(
        (this.currentPage - 1) * 10,
        this.currentPage * 10
      );
    }
  },
  methods: {
    handleCurrentChange(page){
        console.log(page)
        this.currentPage = page;
    }
  },
  mounted() {
        const loading = this.$loading({
            lock: true,
            text: '获取用户列表中',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
        })
        var url = this.HOST + "/wx_mini/getUserList";
        $.get(url)
        .then(response => {
            log(JSON.stringify(response))
            this.memberList = response
        })
        .catch(err => {
            
        })
        .always(() => {
            loading.close();
        })
  }
}
</script>

<style scoped>

#MemberManage {
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

</style>
