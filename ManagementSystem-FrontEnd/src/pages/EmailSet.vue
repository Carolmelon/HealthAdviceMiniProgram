<template>
  <div id="EmailSet">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        <div style="padding:30px;">
            <div style="width:250px;text-align:left;">
                <div style="padding:20px;">当前通知邮箱：</div>
                <div style="margin-left:30px;">
                    <el-input
                        placeholder="请选择日期"
                        suffix-icon="el-icon-bell"
                        v-model="email">
                    </el-input>
                </div>
                <div style="padding:20px;">
                    <el-button @click="changeEmail" type="primary" plain>修改邮箱</el-button>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmailSet',
  data() {
      return {
          email: ""
      }
  },
  computed: {
    
  },
  methods: {
    changeEmail() {
        var url = this.HOST + "/wx_mini/setEmail";
        $.post(url,{
            email:this.email
        })
        .then(response => {
            log(JSON.stringify(response))
            this.email = response
        })
        .catch(err => {
            
        })
        .always(() => {
            // loading.close();
        })
    }
  },
  mounted() {
      var url = this.HOST + "/wx_mini/getEmail";
        $.get(url)
        .then(response => {
            log(JSON.stringify(response))
            this.email = response
        })
        .catch(err => {
            
        })
        .always(() => {
            // loading.close();
        })
  }
}
</script>

<style scoped>

#EmailSet {
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
