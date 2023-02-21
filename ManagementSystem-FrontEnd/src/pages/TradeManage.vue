<template>
  <div id="TradeManage">
    <div class="inner-top"></div>
    <div class="inner-bottom">
        <div class="buttons" style="height:55px;">
            <el-button class="inline-button" @click="exportList" type="success" plain>导出数据</el-button>
            <div class="inline-button" style="width: 10px; height: 40px; border-left: 3px solid #ddd"></div>
            <el-button class="inline-button" @click="seeAllTrades" type="success" plain>查看全部</el-button>
            <el-select @change="searchByTel" class="inline-button" v-model="searchTel" placeholder="按手机号选择">
                <el-option
                v-for="item in telephones"
                :key="item"
                :label="item"
                :value="item">
                </el-option>
            </el-select>
            <div class="inline-button" style="width: 10px; height: 40px; border-left: 3px solid #ddd"></div>
            <div class="inline-button">
                <el-input v-model="searchOpenid" placeholder="按用户id搜索"></el-input>
            </div>
            <el-button class="inline-button" @click="searchByOpenid" type="info" plain>搜索</el-button>
            <div class="inline-button" style="width: 10px; height: 40px; border-left: 3px solid #ddd"></div>
        </div>

        <div style="height: 50px; background-color:#aaa;position:relative;padding-top:10px;">
            <b style="position:absolute;left:30px;">订单号</b>
            <b style="position:absolute;left:25%;">用户id</b>
            <b style="position:absolute;left:37%;">手机号</b>
            <b style="position:absolute;left:45%;">支付金额</b>
            <b style="position:absolute;left:55%;">下单时间</b>
            <b style="position:absolute;left:68%;">订单状态</b>
            <b style="position:absolute;left:78%;">支付时间</b>
            <b style="position:absolute;left:93%;">查看</b>
        </div>

        <div class="table" style="padding: 20px;">
            <div v-for="item in currentPageTrade" :key="item.id"
                style="height:40px;position:relative;padding-top:10px;border-bottom:1.5px solid #ccc">
                <span style="position:absolute;left:5px;">{{item.oid}}</span>
                <span style="position:absolute;left:18%;font-size:10px;">{{item.openid}}</span>
                <span style="position:absolute;left:35%;">{{item.phone}}</span>
                <span style="position:absolute;left:46%;">{{item.total_price}}</span>
                <span style="position:absolute;left:53%;">{{item.order_time}}</span>
                <span style="position:absolute;left:70%;">{{item.trade_status_text}}</span>
                <span style="position:absolute;left:80%;">{{item.pay_time}}</span>
                <span style="position:absolute;left:95%;">
                    <el-button
                        type="text"
                        size="mini"
                        @click="switchDetails(item.oid)">
                        查看
                    </el-button>
                </span>
            </div>  
        </div>

        <div style="padding-bottom: 50px; padding-top: 50px;">
            <el-pagination
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-size="10"
                layout="total, prev, pager, next, jumper"
                :total="TradeListData.length">
            </el-pagination>
        </div>
    </div>

    
    <div id="tradeDetails" style="position:fixed;left:0;right:0;bottom:0;top:0;background: rgba(0,0,0,0.7);display:none;">
        <!-- 编辑订单信息 -->
        <div v-loading="detailLoading"
        style="width:1000px;height:80%;background-color:#fff;margin:50px auto;position:relative;border-radius:20px;overflow:auto;padding-bottom:70px;">
            <el-button @click="switchDetails(null)" style="position:absolute;right:10px;top:60px;" type="primary" plain>关闭</el-button>
            <el-button @click="changeTradeDataMethod(tradeDetails.trade_id)" style="position:absolute;right:10px;top:110px;" type="info" plain>保存并关闭</el-button>
            <el-button @click="deleteTradeDataMethod(tradeDetails.trade_id)" style="position:absolute;right:10px;top:160px;" type="danger" plain>删除订单</el-button>

            <div style="min-height:60px;margin:20px;text-align:left;width:800px;">
                <div style="height:30px;font-size:17px;">
                    <span style="width:10px;height:22px;background-color:#409EFF;display:inline-block;border-radius:5px;position:relative;top:5px;"></span>
                    产品信息
                </div>
                <div style="height:90px;">
                    <div style="height:30px;background-color: #ddd;border-radius:5px;padding-top:5px;">
                        <!-- 产品图片	商品名称	价格	数量	共 -->
                        <b style="width:250px;display:inline-block;padding-left:20px;">产品图片</b>
                        <b style="width:250px;display:inline-block;">商品名称</b>
                        <b style="width:100px;display:inline-block;">价格</b>
                        <b style="width:100px;display:inline-block;">数量</b>
                        <b style="width:80px;display:inline-block;">共</b>
                    </div>
                    <div style="min-height:60px;border-bottom:1px solid #eee; position:relative">
                        <img v-if="tradeDetails.product_img" width="50" height="50" style="margin:5px;margin-left:20px;margin-right:180px;" :src="HOST + tradeDetails.product_img" alt="">
                        <div style="position:absolute;top:20px;left:250px">
                            <span style="width:250px;display:inline-block;">{{tradeDetails.product_name}}</span>
                            <span style="width:100px;display:inline-block;">{{tradeDetails.product_price}}</span>
                            <span style="width:100px;display:inline-block;">{{tradeDetails.amount}}</span>
                            <span style="width:80px;display:inline-block;">{{tradeDetails.cal_total_price}}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div style="min-height:60px;margin:20px;text-align:left;width:800px;">
                <div style="height:30px;font-size:17px;">
                    <span style="width:10px;height:22px;background-color:#409EFF;display:inline-block;border-radius:5px;position:relative;top:5px;"></span>
                    订单信息
                </div>
                <div style="min-height:90px;padding-top:20px;">
                    <div style="height:40px;border-bottom:1px solid #eee;border-top:1px solid #eee;">
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            订单号: {{tradeDetails.trade_id}}
                        </div>
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            用户id: {{tradeDetails.openid}}
                        </div>
                    </div>
                    <div style="height:40px;border-bottom:1px solid #eee;">
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            电话号码: {{tradeDetails.tel}}
                        </div>
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            下单时间: {{tradeDetails.order_time}}
                        </div>
                    </div>
                    <div style="min-height:40px;border-bottom:1px solid #eee;">
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            支付时间: {{tradeDetails.pay_time}}
                        </div>
                        <div style="width:400px;float:left;line-height:40px;padding-left:30px;">
                            实付金额: <span style="color:red">￥{{tradeDetails.now_total_price}}</span>
                        </div>
                    </div>
                    <div style="clear:both;"></div>
                    <!-- 下单留言: {{tradeDetails.liuyan}} now_total_price -->
                    <div style="min-height:40px;border-bottom:1px solid #eee;line-height:40px;padding-left:30px;">
                        下单留言: {{tradeDetails.liuyan}}
                    </div>
                    <div style="min-height:40px;border-bottom:1px solid #eee;line-height:40px;padding-left:30px;">
                        价格调整：<el-input @blur="handlerChangePriceForm" v-bind:value="changeTradeData.changePrice" size="mini" style="width:200px;" placeholder="请输入内容"></el-input>
                        <span style="font-size:10px;color:#888">可正可负，单位为元</span>
                    </div>
                    <div style="min-height:60px;border-bottom:1px solid #eee;line-height:60px;padding-left:30px;">
                        订单状态：
                        <el-select style="width:200px;height:30px;" v-model="tradeDetails.trade_status" placeholder="请选择">
                            <el-option
                            v-for="item in static_trade_status"
                            :key="item.id"
                            :label="item.text"
                            :value="item.id">
                            </el-option>
                        </el-select>
                    </div>
                    
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "TradeManage",
  data() {
    return {
      telephones: [
        "选项1"
      ],
      searchTel: "",
      searchOpenid: "",
      TradeListData: [
        {
          a: 1,
          b: 2,
          c: 3,
          d: 4,
          e: 5,
          f: 6,
          g: 7
        }
      ],
      currentPage: 1,
      //   currentPageTrade: [], // 暂时的
      detailLoading: true,
      tradeDetails: {},
      changeTradeData: {
          changePrice: "0.00",
      },
      static_trade_status: [
          {text: "未支付", id: 1},
          {text: "待收货", id: 2},
          {text: "已完成", id: 3},
          {text: "已退款", id: 4},
      ],
    };
  },
  computed: {
    currentPageTrade() {
      return this.TradeListData.slice(
        (this.currentPage - 1) * 10,
        this.currentPage * 10
      );
    }
  },
  methods: {
    exportList(e) {
      console.log(e);
    },
    seeAllTrades(e) {
        this.searchOpenid = ""
        this.searchTel = ""
        this.refreshTradeList()
    },
    searchByTel(e) {
        console.log(e);
        this.searchOpenid = "";
        this.refreshTradeList()
    },
    searchByOpenid(e) {
        this.searchTel = ""
        console.log(this.searchOpenid);
        this.refreshTradeList()
    },
    refreshTradeList() {
      // articleListData
      const loading = this.$loading({
        lock: true,
        text: "获取订单列表中",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
      var url = this.HOST + "/wx_mini/getTradeListData?searchTel=" + this.searchTel +
      "&searchOpenid=" + this.searchOpenid;
      $.get(url)
        .then(response => {
          log(response)
          this.TradeListData = JSON.parse(JSON.stringify(response));
        })
        .catch(err => {
          log(err);
        })
        .always(() => {
          loading.close();
        });
      // articleListData
    },
    handleCurrentChange(page) {
      console.log(page);
      this.currentPage = page;
    },
    switchDetails(oid) {
      var DetailsDiv = document.getElementById("tradeDetails");
      if (DetailsDiv.style.display === "none") {
        this.detailLoading = true;
        DetailsDiv.style.display = "block";
        if (oid !== null) {
          // 打开详情页
          // console.log(oid)
          var url = this.HOST + "/wx_mini/getTradeDetailsById?trade_id=" + oid;
          $.get(url)
            .then(response => {
              // log(response)
              console.log(response);
              this.tradeDetails = response;
            })
            .catch(err => {
              log(err);
              DetailsDiv.style.display = "none";
            })
            .always(() => {
              this.detailLoading = false;
            });
        }
      } else {
        DetailsDiv.style.display = "none";
        this.changeTradeData.changePrice = "0.00"
      }
    },
    handlerChangePriceForm(e) {
        var value = Number(e.target.value)
        var newValue = Math.round(value * 100) / 100
        if(isNaN(newValue))
            newValue = 0.00
        console.log(newValue)
        this.changeTradeData.changePrice = Number(newValue).toFixed(2)
    },
    changeTradeDataMethod(oid) {
        this.$confirm('确定要修改订单吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            var data = {
                changePrice: this.changeTradeData.changePrice,
                trade_status: this.tradeDetails.trade_status,
                oid: oid,
            }
            const loading = this.$loading({
                lock: true,
                text: '修改中...',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            var url = this.HOST + "/wx_mini/changeTradeData";
            $.post(url,{
                data: JSON.stringify(data)
            })
            .then(response => {
                log(response)
                if(response.success === true){
                    this.$message({
                        type: 'success',
                        message: '修改成功!'
                    });
                    this.changeTradeData.changePrice = "0.00"
                    var DetailsDiv = document.getElementById("tradeDetails");
                    DetailsDiv.style.display = "none";
                    this.refreshTradeList()
                }else{
                    this.$message({
                        type: 'info',
                        message: response.err_msg
                    });
                }
            })
            .catch(err => {
            log(err);
            })
            .always(() => {
                loading.close();
            });
            console.log(data);
        }).catch(_=>{
            console.log("取消修改")
        })
        .finally(_=>{
            console.log("any")
            // this.changeTradeData.changePrice = "0.00"
        });
    },
    deleteTradeDataMethod(oid) {
        this.$confirm('此操作将永久删除该订单, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            const loading = this.$loading({
                lock: true,
                text: '删除中...',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            var url = this.HOST + "/wx_mini/deleteTradeData";
            $.post(url,{
                oid: oid
            })
            .then(response => {
                log(response)
                if(response.success === true){
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    });
                    this.changeTradeData.changePrice = "0.00"
                    var DetailsDiv = document.getElementById("tradeDetails");
                    DetailsDiv.style.display = "none";
                    this.refreshTradeList()
                }else{
                    this.$message({
                        type: 'info',
                        message: response.err_msg
                    });
                }
            })
            .catch(err => {
            log(err);
            })
            .always(() => {
                loading.close();
            });
            console.log(data);
        }).catch(() => {
          console.log("取消删除")         
        });
    },
    loadAllTels() {
        var url = this.HOST + "/wx_mini/getAllTels"
        $.get(url)
        .then(response => {
            // log(response)
            // console.log(response)
            this.telephones = response
        })
        .catch(err => {
            log(err);
        })
        .always(() => {
            
        });
    }
  },
  mounted() {
    window.a = this;
    this.refreshTradeList();
    this.loadAllTels()
  }
};
</script>

<style scoped>
#TradeManage {
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

.inline-button {
  float: left;
  margin: 10px;
  /* height: 100%; */
}
</style>
