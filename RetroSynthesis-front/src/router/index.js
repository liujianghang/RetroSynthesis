import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/HomePages/Home";
import retro from "../components/RetroPages/Retro";
import Login from "../components/HomePages/Login";
import Register from "../components/HomePages/register";
import requests from "../api/request";
import request from "../api/request";

Vue.use(Router)

const routes = [
  {
    path: '/',
    component: Home,
    name: 'home'
  },
  {
    path: '/retro',
    component: retro,
    name: 'retro'
  },
  {
    path: '/login',
    component: Login,
    name: 'login'
  },
  {
    path: '/register',
    component: Register,
    name: 'register'
  },
  {
    path: '*',
    component: Home
  }
]

const router = new Router({
  routes
})
// 路由拦截
// router.beforeEach((to, from, next) => {
//   let token = localStorage.getItem('token')
//   if (token) {
//
//   }
//   next()
// })

export default router

