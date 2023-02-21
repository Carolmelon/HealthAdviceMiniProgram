<template>
  <div id="Asides">
      <el-tree class="trees"
        :data="data"
        :props="defaultProps"
        accordion
        @node-click="handleNodeClick"
        highlight-current>
      </el-tree>
      <!-- <div class="float-div">
        <p><router-link to="/allGoods">已有商品</router-link></p>
      </div> -->
      
  </div>
</template>

<script>
export default {
  name: "Asides",
  data() {
    return {
      data: [
        {
          label: "站点概况"
        },
        {
          label: "文章",
          children: [
            {
              label: "添加文章"
            },
            {
              label: "文章管理"
            },
            {
              label: "文章分类"
            },
            // {
            //   label: "标签管理"
            // },
            {
              label: "文章仓库"
            }
          ]
        },
        {
          label: "产品",
          children: [
            {
              label: "添加产品"
            },
            {
              label: "产品管理"
            },
            {
              label: "管理分类"
            },
            // {
            //   label: "批量导入"
            // },
            {
              label: "产品仓库"
            },
            // {
            //   label: "标签管理"
            // }
          ]
        },
        {
          label: "订单",
          children: [
            {
              label: "订单管理"
            }
          ]
        },
        {
          label: "留言",
          children: [
            {
              label: "留言管理"
            }
          ]
        },
        {
          label: "会员",
          children: [
            // {
            //   label: "会员管理"
            // }
          ]
        },
        {
          label: "设置接收通知邮箱",
          children: [
            // {
            //   label: "会员管理"
            // }
          ]
        }
      ],
      defaultProps: {
        children: "children",
        label: "label",
      }
    };
  },
  mounted() {},
  methods: {
    handleNodeClick(data) {
      console.log(data.$treeNodeId);
      // 侧边栏跳转界面
      if(data.$treeNodeId == 1){
        this.$router.push({path: '/'})
        return;
      }
      if(data.$treeNodeId == 3){
        this.$router.push({path: '/AppendArticle'})
        return;
      }
      if(data.$treeNodeId == 4){
        this.$router.push({path: '/ManageArticle'})
        return;
      }
      if(data.$treeNodeId == 5){
        this.$router.push({path: '/ClassifyArticle'})
        return;
      }
      if(data.$treeNodeId == 6){
        this.$router.push({path: '/ArticleHouse'})
        return;
      }
      //文章结束 产品开始
      if(data.$treeNodeId == 8){
        this.$router.push({path: '/AddProduct'})
        return;
      }
      if(data.$treeNodeId == 9){
        this.$router.push({path: '/ManageProduct'})
        return;
      }
      if(data.$treeNodeId == 10){
        this.$router.push({path: '/ClassifyProduct'})
        return;
      }
      // if(data.$treeNodeId == 11){
      //   this.$router.push({path: '/ImportProduct'})
      //   return;
      // }
      if(data.$treeNodeId == 11){
        this.$router.push({path: '/ManagePdtQuality'})
        return;
      }
      //     import TradeManage from '@/pages/TradeManage'
      //     import MessageManage from '@/pages/MessageManage'
      //     import MemberManage from '@/pages/MemberManage'
      //     import EmailSet from '@/pages/EmailSet'
      if(data.$treeNodeId == 13){
        this.$router.push({path: '/TradeManage'})
        return;
      }
      if(data.$treeNodeId == 15){
        this.$router.push({path: '/MessageManage'})
        return;
      }
      if(data.$treeNodeId == 16){
        this.$router.push({path: '/MemberManage'})
        return;
      }
      if(data.$treeNodeId == 17){
        this.$router.push({path: '/EmailSet'})
        return;
      }
    }
  }
};
</script>

<style scoped>
#Asides {
  background-color: slategray;
}

.trees {
  background-color: slategray;
  color: orange;
}


</style>
