<template>
  <section>
    <nav class="navbar navbar-expand-md navbar-dark bg-info my-navbar" role="navigation">
      <!--    标签头    -->
      <router-link to="/" class="navbar-brand" style="padding: 5px 5px 0px">
        <img src="../../assets/img/logo.png" width="35" height="35" class="d-inline-block " alt="">
        BioRetro
      </router-link>
      <!--    全部的标签    -->
      <div class="collapse navbar-collapse ">
        <!--    Home，Retro，About us  -->
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item active">
            <router-link to="/retro" class="nav-link">Retro</router-link>
          </li>
          <li class="nav-item active">
            <span class="nav-link" @click="goto(url.biod)">About us</span>
          </li>
        </ul>

        <!--    Login    -->
        <ul class="navbar-nav justify-content-end">
          <li class="nav-item active" v-if="username">
            <router-link to="" class="nav-link">{{ username }}</router-link>
          </li>
          <li class="nav-item active" v-if="username">
            <span class="nav-link" @click="logout">Logout</span>
          </li>
          <li class="nav-item active" v-if="!username">
            <router-link to="/login" class="nav-link" @click="logout">Login</router-link>
          </li>
          <li class="nav-item active" v-if="!username">
            <router-link to="/register" class="nav-link">Register</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </section>
</template>

<script>

export default {
  name: 'Navbar',  //this is the name of the component
  data() {
    return {
      username: '',
      url: {
        biod: "http://biod.whu.edu.cn/",
      }
    }
  },
  methods: {
    goto(e) {
      window.open(e, '_blank')
    },
    logout() {
      // localStorage.removeItem('token')
      // localStorage.removeItem('userId')
      this.username = ''
      this.$router.push('/login')
      location.reload()
    }
  },
  mounted() {
    if (this.$route.path !== '/login'&&this.$route.path !== '/register') {
      this.username = localStorage.getItem('userId')
    }
  }
}
</script>
<style>

.my-navbar {
  /*background-color: #c3f3f6;*/
  margin-top: 10px;
  padding: 10px 10px;
  border-radius: 10px;
}

span:hover {
  cursor: pointer;
}
</style>
