import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        // allTrade: [],
        // allGoods: [],
        // batch: [],
        // changeGoodsInfo: {
        //     name: "", // 不可更改
        //     desc: "",
        //     imgUrl: "",
        //     price: "",
        //     leave: "",
        // }
    },
    mutations: {
        // initialAllTrade(state, allTrade){
        //     state.allTrade = allTrade;
        // },
    },
    actions: {
        // initialAllTrade(context, allTrade) {
        //     context.commit('initialAllTrade', allTrade)
        // },
    }
})