<template>
  <div class="container">
    <h1>Input</h1>

    <h4>Custom</h4>
    <!--   Input   -->
    <form action="">
      <fieldset class="form-row">
        <div class="form-group col-sm-4 offset-md-1">
          <label for="mol">Target compound(SIMLES)<span style="color: #dc3545">*</span>:</label>
          <input type="text" id="mol" v-model.trim="submitForm.target" class="form-control"
                 v-bind:class="{'is-invalid': submitForm.error1,'is-valid':submitForm.success1}"
                 placeholder="Input a SMILES">
          <div v-if="submitForm.error1" class="invalid-feedback">{{ submitForm.error1 }}</div>
          <div v-if="submitForm.success1" class="valid-feedback">{{ submitForm.success1 }}</div>
        </div>
        <div class="form-group col-sm-2 offset-md-1">
          <label for="iterations">Iterations:</label>
          <input type="text" id="iterations" v-model.trim="submitForm.iterations" class="form-control"
                 v-bind:class="{'is-invalid': submitForm.error2,'is-valid':submitForm.success2}" placeholder="1~3000">
          <div v-if="submitForm.error2" class="invalid-feedback">{{ submitForm.error2 }}</div>
        </div>
        <div class="form-group col-sm-2 offset-md-1">
          <label for="expansion_topk">Expansion topk:</label>
          <input type="text" id="expansion_topk" v-model.trim="submitForm.expansion_topk" class="form-control"
                 v-bind:class="{'is-invalid': submitForm.error3,'is-valid':submitForm.success3}" placeholder="50">
          <div v-if="submitForm.error3" class="invalid-feedback">{{ submitForm.error3 }}</div>
        </div>
        <button type="submit" class="btn btn-info btn-block my-btn-1" @click="submitByAxios"><span
          v-bind:class="{'spinner-border spinner-border-sm': submitForm.isLoading}"></span>&nbsp{{
            submitForm.submitText
          }}&nbsp
        </button>
      </fieldset>
    </form>


    <h4>Just Try</h4>
    <fieldset class="form-row ">
      <div class="col-sm-3 offset-2 ">
        <button type="submit" class="btn btn-info my-btn-2" @click="passLocalData1">CCC(=O)O</button>
      </div>
      <div class="col-sm-3 offset-2">
        <button type="submit" class="btn btn-info my-btn-2" @click="passLocalData2">[NH]1CCCC1</button>
      </div>
    </fieldset>
  </div>
</template>

<script>
import bus from "../../assets/js/eventBus";
import requests from "../../api/request";


export default {
  name: "Input",
  data() {
    return {
      // sharedState: store.state,
      submitForm: {
        target: null,
        iterations: 3000,
        expansion_topk: 50,
        error1: null,
        error2: null,
        error3: null,
        success1: null,
        success2: null,
        success3: null,
        errorsCount: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        isLoading: false,  //是否处于等待状态
        submitText: 'Get Path !', // 上传按钮的内容
      },
      resultInfo: null,
      localData: null,
    }
  },
  methods: {
    submitByAxios() {
      this.submitForm.errorsCount = 0

      // 验证target_mol
      if (!this.submitForm.target) {
        this.submitForm.errorsCount++
        this.submitForm.error1 = 'You must input a valid SIMLES.'
      } else {
        this.submitForm.error1 = null
      }
      // 验证target_iterations
      if (!this.submitForm.iterations || isNaN(this.submitForm.iterations)) {
        this.submitForm.errorsCount++
        this.submitForm.error2 = 'You must input a valid iteration number.'
      } else {
        this.submitForm.error2 = null
      }
      // 验证expansion_topk
      if (!this.submitForm.expansion_topk || isNaN(this.submitForm.expansion_topk)) {
        this.submitForm.errorsCount++
        this.submitForm.error3 = 'You must input a valid expansion topk number.'
      } else {
        this.submitForm.error3 = null
      }
      // 表单验证没通过时，不继续往下执行
      if (this.submitForm.errorsCount > 0) {
        return false
      }

      // 通过表单验证后
      const path = '/retro/plan'
      const username = localStorage.getItem("username")
      const param = {
        'target_mol': this.submitForm.target.toUpperCase(),
        'target_iterations': this.submitForm.iterations,
        'expansion_topk': this.submitForm.expansion_topk,
        'username': username
      }
      this.submitForm.isLoading = true
      this.submitForm.submitText = 'loading...'
      // 使用axios发送数据

      requests.post(path, param)
        .then((response) => {
          if (response.data.code === 200) {
            this.successInput()
            let result = response.data.data
            this.passData(result)
          }
          if (response.data.code === 500) {
            alert("服务器错误")
          }
          if (response.data.code === 401) {
            alert("请先登录！")
            // 在弹窗确认后跳转到指定页面
            // this.$router.push('/login');
          }
          if (response.data.code === 400 && response.data.msg === 'wrong') {
            this.wrongInput()
          }
          if (response.data.code === 404 && response.data.msg === 'basic') {
            this.basicInput()
          }
        })
        .catch((error) => {
          console.log(error.response)
        })
    },
    successInput() {
      this.submitForm.isLoading = false
      this.submitForm.submitText = 'Get Path'
      this.submitForm.success1 = 'success!'
    },
    wrongInput() {
      this.submitForm.isLoading = false
      this.submitForm.success1 = null
      this.submitForm.error1 = 'This is a invalid SMILE or the system can\'t find the path, please retry.'
      this.submitForm.submitText = 'Get Path'
    },
    basicInput() {
      this.submitForm.isLoading = false
      this.submitForm.success1 = null
      this.submitForm.error1 = 'This is a basic block, please retry.'
      this.submitForm.submitText = 'Get Path'
    },
    passData(data) {
      bus.$emit('sendResultData', data.all_routes)
      bus.$emit('sendShowData', [data.elements, data.cids, data.best_edges, data.r_map, data.target_mol, data.build_blocks])
      // bus.$emit('sendCidData',)
    },
    // test
    passLocalData1() {
      this.passData(this.localData.try1)
    },
    passLocalData2() {
      this.passData(this.localData.try2)
    },
    readLocalData() {
      const localJson = requests.create({
        baseURL: '',
        timeout: 10000,
      })
      localJson.get('../../static/data/try.json').then(res => {
        this.localData = res.data
      })
    }
  },
  mounted() {
    this.readLocalData()
  }
}
</script>

<style scoped>
fieldset {
  width: 100%;
  height: auto;
  border: 1px solid #17a2b8;
  border-radius: 10px;
  padding-top: 20px;
  margin-bottom: 15px;
}

label {
  /*font-weight: bold;*/
  font-size: larger;
}

.my-btn-1 {
  width: 25%;
  height: 50px;
  vertical-align: middle;
  text-align: center;
  /*font-size: 23px;*/
  margin: 10px auto 40px
}

.my-btn-2 {
  width: 100%;
  vertical-align: middle;
  text-align: center;
  margin: 10px auto 30px
}


</style>
