<template>

  <div class="main-bg">

<!--    <div class="box-conatiner">-->

      <div class="row">
        <div class="col-md-6 col-sm-6">
          <h1 class="heading-left">For Continue Please Login</h1>
        </div>
        <div class="col-sm-6 col-md-6">
          <div class="wrap-login100"><span class="login100-form-title">Sign In</span>
            <form class="login100-form p-l-55 p-r-55 p-t-20">

              <!--       账户和密码       -->
              <div class="form-group">
                <input type="text" v-model.trim="username" class="form-control"
                       v-bind:class="{'is-invalid': username_error,'is-valid':isSuccess}"
                       placeholder="username" @blur="check_username">
                <div v-if="username_error" class="invalid-feedback">{{ username_error }}</div>
              </div>
              <div class="form-group">
                <input type="password" v-model.trim="password" class="form-control"
                       v-bind:class="{'is-invalid': password_error,'is-valid':isSuccess}" placeholder="password">
                <div v-if="password_error" class="invalid-feedback">{{ password_error }}</div>
              </div>

              <!--       记住我       -->
              <div class="form-check mb-2 mr-sm-2">
                <label class="form-check-label">
                  <input class="form-check-input" v-model="checked" type="checkbox"> Remember me
                </label>
              </div>

              <!--     如果忘记了密码       -->
<!--              <div class="text-right p-t-13 p-b-23"><span class="txt1">Forgot</span>-->
<!--                <a href="#" class="txt2">username / password?</a>-->
<!--              </div>-->
              <!--      登录和注册按钮        -->
              <div>
                <button class="login100-form-btn" id="signIn" @click="login_user">Sign in</button>
              </div>
              <router-link to="/register" class="flex-col-c p-t-140 p-b-40 txt2">Register now</router-link>
            </form>
          </div>
        </div>
      </div>
    </div>
<!--  </div>-->
</template>

<script>
import {Base64} from 'js-base64'
import requests from "../../api/request";

export default {
  name: "Login",
  data() {
    return {
      isSuccess: false,
      username: '',
      password: '',
      username_error: '',
      password_error: '',
      checked: true
    }
  },
  mounted() {
    let username = localStorage.getItem("userId");
    if (username) {
      try {
        this.username = localStorage.getItem("userId")
        this.password = Base64.decode(localStorage.getItem("password"));// base64解密
        this.checked = true;
      } catch (err) {
      }
    }
  },
  methods: {
    login_user() {
      // 检查登录
      if (!this.check_login()) {
        return false
      }

      // 检查勾选
      this.if_check()

      let params = {
        "username": this.username,
        "password": this.password,
      }
      //发送成功后
      requests.post('/user/login', params, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
        .then(response => {
          if (response.data.code === 200) {
            // localStorage.setItem("userId", this.username);
            // localStorage.setItem("password",this.password)
            this.resetAll()
            this.isSuccess = true
            // let password = Base64.encode(this.password); // base64加密
            let token = response.headers.get("token")
            localStorage.setItem("token", token);
            this.$router.push('retro')
            window.location.reload();
          } else if (response.data.code === 400) {
            this.username_error = '用户名不存在或密码错误！'
            this.username = ''
          } else {
            alert('登录失败,请重试！')
            this.resetAll()
          }
        })
      this.isSuccess = true
    },
    check_username() {
      let str = this.username
      let check_flag = true
      // 先检查是不是邮箱
      let string = str.replace(/\s|&nbsp;/g, '') // 先去除用户输入的无效字符
      let reg = /^[a-zA-Z]\w{5,19}$/         //  首位是字母 长度为6-20
      if (reg.test(string)) {
        check_flag = true
      } else {
        check_flag = false
      }
      if (check_flag === true) {
        this.username_error = ''
      } else {
        this.username_error = '请输入正确的账号，账号首位为字母'
      }
    },
    if_check() {
      if (this.checked) {
        let password = Base64.encode(this.password); // base64加密
        localStorage.setItem("userId", this.username);
        localStorage.setItem("password", password);
      } else {
        localStorage.removeItem("userId");
        localStorage.removeItem("password");
      }
    },
    check_login() {
      if (this.username === '') {
        this.username_error = '账号不能为空！'
        this.password_error = ''
        return false
      }
      if (this.password === '') {
        this.password_error = '密码不能为空！'
        return false
      }
      this.username_error = ''
      this.password_error = ''
      return true
    },
    resetAll() {
      this.isSuccess = false
      this.username = ''
      this.password = ''
      this.username_error = ''
      this.password_error = ''
    }
  }
}
</script>
<!--<style scoped >-->
<style scoped src="@/assets/css/style.css">


</style>
