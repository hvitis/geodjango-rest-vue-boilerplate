import Vue from 'vue'
import Vuex from 'vuex'
import posts from './modules/posts'
import accounts from './modules/accounts'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    posts,
    accounts
  }
})