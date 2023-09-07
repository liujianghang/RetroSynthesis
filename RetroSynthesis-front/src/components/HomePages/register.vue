<template>

  <div class="main-bg">
<!--    <div class="box-conatiner">-->
      <div class="row">
        <div class="col-md-6 col-sm-6">
          <h1 class="heading-left">For Continue Please Register</h1>
        </div>
        <div class="col-sm-6 col-md-6">
          <div class="wrap-login100">
            <span class="login100-form-title">Register</span>
            <form class="login100-form p-l-55 p-r-55 p-t-20">


              <div class="form-group ">
                <input type="text" v-model.trim="username" class="form-control my-border"
                       v-bind:class="{'is-invalid': username_error,'is-valid':isSuccess}" placeholder="username"
                       @blur="check_username">
                <div v-if="username_error" class="invalid-feedback">{{ username_error }}</div>
              </div>
              <div class="form-group">
                <input type="email" v-model.trim="email" class="form-control"
                       v-bind:class="{'is-invalid': email_error,'is-valid':isSuccess}" placeholder="email"
                       @blur="check_email">
                <div v-if="email_error" class="invalid-feedback">{{ email_error }}
                </div>
              </div>
              <div class="form-group">
                <input type="password" v-model.trim="password" class="form-control"
                       v-bind:class="{'is-invalid': password_error,'is-valid':isSuccess}" placeholder="password"
                       @blur="check_password">
                <div v-if="password_error" class="invalid-feedback">{{ password_error }}
                </div>
              </div>
              <div class="form-group">
                <input type="password" v-model.trim="confirmPassword" class="form-control"
                       v-bind:class="{'is-invalid': confirmPassword_error,'is-valid':isSuccess}"
                       placeholder="confirm password" @blur="check_confirm_password">
                <div v-if="confirmPassword_error" class="invalid-feedback">{{ confirmPassword_error }}
                </div>
              </div>
              <div>
                <button class="login100-form-btn" @click="register">Register</button>
              </div>
              <router-link to="/login" class="flex-col-c p-t-140 p-b-40 txt2">Login</router-link>
            </form>
          </div>
        </div>
      </div>
    </div>
<!--  </div>-->
</template>

<script>
import requests from "../../api/request";
import {Base64} from "js-base64";

export default {

  name: "register",
  data() {
    return {
      isSuccess: false,
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      username_error: '',
      email_error: '',
      password_error: '',
      confirmPassword_error: ''
    }
  },
  methods: {
    register() {
      if (this.check_username() && this.check_email() && this.check_password() && this.check_confirm_password()) {
        // alert('注册成功')
        let data = {
          "username": this.username,
          "email": this.email,
          "password": this.password
        }
        requests.post('/user/register', data, {headers: {'Content-Type': 'application/json'}})
          .then(response => {
            if (response.data.code === 200) {
              this.isSuccess = true
              this.resetAll()
              let password = Base64.encode(this.password); // base64加密
              localStorage.setItem("userId", this.username);
              localStorage.setItem("password", password);
              this.$router.push('/login')
            } else if (response.data.code === 400) {
              this.username_error = '该用户名已存在！'
            } else {
              alert('注册失败,请重试！')
              this.resetAll()
            }
          })
      }
    },
    check_email() {
      let str = this.email
      // 先检查是不是邮箱
      let string = str.replace(/\s|&nbsp;/g, '') // 先去除用户输入的无效字符
      let reg = /^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
      if (!reg.test(string)) { // 如果是邮箱
        this.email_error = '请输入正确的邮箱！'
        return false
      } else {
        this.email_error = ''
        return true
      }
    },
    check_username() {
      let str = this.username
      let reg = /^[a-zA-Z]\w{5,19}$/         //  首位是字母 长度为6-20
      let string = str.replace(/\s|&nbsp;/g, '') // 先去除用户输入的无效字符
      if (!reg.test(string)) {
        this.username_error = '用户名首位必须为字母，长度为6-20位！'
        return false
      } else {
        this.username_error = ''
        return true
      }
    },
    check_password() {
      let str = this.password
      let length = str.length
      if (length < 6 || length > 20) {
        this.password_error = '密码长度必须是6-20位！'
        return false
      } else {
        this.password_error = ''
        return true
      }
    },
    check_confirm_password() {
      let str1 = this.password
      let str2 = this.confirmPassword
      if (str1 !== str2) {
        this.confirmPassword_error = '密码和确认密码不一致！'
        return false
      } else {
        this.password_error = ''
        this.confirmPassword_error = ''
        return true
      }
    },
    resetAll() {
      this.email = ''
      this.email_error = ''
      this.username = ''
      this.username_error = ''
      this.email = ''
      this.email_error = ''
      this.password = ''
      this.password_error = ''
      this.confirmPassword = ''
      this.confirmPassword_error = ''
    }
  }
}
</script>
<!--<style scoped >-->
<style scoped src="@/assets/css/style.css">


</style>
