import axios from "axios";

const requests = axios.create({
  baseURL: 'http://127.0.0.1:8080/api',
  timeout: 100000
})
requests.interceptors.request.use(config => {
    config.headers.token = localStorage.getItem('token')
    console.log(config.headers.token)
    return config
  },
  error => {
    return Promise.reject(error)
  })

// requests.interceptors.response.use(response => {
//   let token = response.headers.token || ''
//   let username = response.headers.username||''
//   if (token) {
//     localStorage.setItem('token', token)
//     localStorage.setItem('username', username)
//   }
//   return response
// }, error => {
//   return Promise.reject(error)
// })

export default requests
