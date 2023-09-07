// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from "./router";
// 导入配置了全局拦截器后的 axios
import axios from 'axios'

// 引入jQuery
import $ from 'jquery'
// 引用bootstrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'font-awesome/css/font-awesome.min.css';
// 引入cytospace
import cytoscape from "cytoscape"



// 将 $axios、$moment  挂载到 prototype 上，在组件中可以直接使用 this.$axios 访问
Vue.prototype.$axios = axios
Vue.prototype.cytoscape = cytoscape
Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
