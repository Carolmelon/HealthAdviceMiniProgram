<template>
  <div id="ClassifyArticle">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        <div class="buttons">
            <el-button @click="addFirstClass" class="button-left" type="primary" icon="el-icon-edit" plain>添加一级分类</el-button>
            <el-button @click="refreshClasses" class="button-left" type="success" icon="el-icon-check" plain>保存更改</el-button>
            <!-- <el-button class="button-left" type="danger" icon="el-icon-delete" plain>删除选中项</el-button> -->
            <!-- <el-button class="button-right" type="info" icon="el-icon-circle-plus" plain>展开</el-button>
            <el-button class="button-right" type="info" icon="el-icon-remove" plain>收起</el-button> -->
        </div>
        <div class="classes">            
            <div style="height: 40px; background-color: #dddddd; padding: 10px">
                <b style="float: left;">分类名</b>
                <b style="float: right; padding-right: 100px;">操作</b>
            </div>
            <div style="clear: both; height: 5px;"></div>
            <el-tree
            :data="options"
            node-key="id"
            default-expand-all
            :expand-on-click-node="false"
            ref="tree"
            draggable>
            <span class="custom-tree-node" slot-scope="{ node, data }">
                <span>{{ node.label }}</span>
                <span>
                <el-button
                    type="text"
                    size="mini"
                    @click="() => rename(data)">
                    重命名
                </el-button>
                <el-button
                    type="text"
                    size="mini"
                    @click="() => append(data)">
                    添加子分类
                </el-button>
                <el-button
                    type="text"
                    size="mini"
                    @click="() => remove(node, data)">
                    删除该分类
                </el-button>
                </span>
            </span>
            </el-tree>

            <!-- <el-tree
            style="border-radius: 20px;overflow: hidden;"
            :data="options"
            node-key="id"
            default-expand-all
            draggable>
            </el-tree> -->
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClassifyArticle',
  data() {
      return {
            options: [
                
            ], //分类数据，在mounted里面初始化
            id: 1000,
      }
  },
  computed: {
    
  },
  methods: {
    append(data) {
        const newChild = { id: this.id++, label: '默认分类名', children: [] };
        if (!data.children) {
            this.$set(data, 'children', []);
        }
        data.children.push(newChild);
    },

    remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
    },

    rename(data) {
        this.$prompt('请输入新分类名', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputValue: data.label,
        }).then(({ value }) => {
            if(!Boolean(value)){
                this.$message({
                    type: 'info',
                    message: '分类名不能为空'
                });
                return;
            }
            data.label = value
        }).catch(() => {
          //什么也不做
        });
    },

    addFirstClass() {
        this.$prompt('请输入新分类名', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputValue: "默认分类名",
        }).then(({ value }) => {
            if(!Boolean(value)){
                this.$message({
                    type: 'info',
                    message: '分类名不能为空'
                });
                return;
            }
            const newChild = { id: this.id++, label: value, children: [] };
            this.options.push(newChild)
        }).catch(() => {
          //什么也不做
        });
    },

    refreshClasses(){
        //打开等待框
        const loading = this.$loading({
            lock: true,
            text: '更新分类中',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
        })
        var url = this.HOST + "/wx_mini/refreshClassifyArticle";
        $.post(url,{
            options: JSON.stringify(this.options),
        })
        .then(response => {
            log(response)
            this.$notify({
                title: '成功',
                message: '更新分类成功',
                type: 'success'
            })
        })
        .catch(err => {
            log(err)
            this.$notify.error({
                title: '错误',
                message: '更新分类失败，请重试或联系管理员'
            })
        })
        .always(() => {
            loading.close();
        })
    },
  },
  mounted() {
      window.a = this;
      const loading = this.$loading({
        lock: true,
        text: '获取分类中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
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
        loading.close();
      })
  }
}
</script>

<style scoped>

#ClassifyArticle {
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

.buttons {
    width: 100%;
    height: 80px;
    padding: 25px 50px 0 50px;
    border-bottom: 5px dotted #eeeeee;
}

.button-left {
    float: left;
}

.button-right {
    float: right;
}

.classes {
    padding: 50px;
    padding-top: 10px;
    border-radius: 20px;
}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}

</style>
