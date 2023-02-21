<template>
  <div id="MessageManage">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        <div style="height:50px;">
            <el-select style="float:left;padding:10px;" @change="changeChildMenu" v-model="child_menu" placeholder="请选择">
                <el-option
                v-for="item in child_menu_lists"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                </el-option>
            </el-select>
        </div>
        <div style="text-align:left;padding-top:20px;padding-bottom:40px;">
            <router-view></router-view>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessageManage',
  data() {
      return {
        child_menu: 1,
        child_menu_lists: [
            {
                value: 1,
                label: "药品代购"
            },
            {
                value: 2,
                label: "专家预约"
            },
            {
                value: 3,
                label: "个人档案"
            },
            {
                value: 4,
                label: "专家建议"
            },
            {
                value: 5,
                label: "图片资料"
            },
        ]
      }
  },
  computed: {
    
  },
  methods: {
    changeChildMenu(){
        console.log(this.child_menu);
        if(this.child_menu === 1){
            this.$router.replace('/MessageManage/ypdg')
        }
        if(this.child_menu === 2){
            this.$router.replace('/MessageManage/zjyy')
        }
        if(this.child_menu === 3){
            this.$router.replace('/MessageManage/grda')
        }
        if(this.child_menu === 4){
            this.$router.replace('/MessageManage/zjjy')
        }
        if(this.child_menu === 5){
            this.$router.replace('/MessageManage/tpzl')
        }
    }
  },
  mounted() {

  }
}
</script>

<style scoped>

#MessageManage {
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
