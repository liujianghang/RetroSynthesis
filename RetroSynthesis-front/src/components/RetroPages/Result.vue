<template>
  <div class="container">
    <h1>Result</h1>
    <table class="table table-striped">
      <thead class="thead-light">
      <tr>
        <th>Pathway</th>
        <th>Length</th>
        <th>Route</th>
      </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
  </div>
</template>

<script>
import bus from "../../assets/js/eventBus";

export default {
  name: "Result",
  data() {
    return {
      resultData: null
    }
  },
  methods: {
    add() {
      const routes = this.resultData;
      const tbody = document.querySelector("tbody")
      $("tbody").empty();
      // 处理数据并添加到表格中
      for (let i = 0; i < routes.length; i++) {
        let route = routes[i];
        let mol_set = new Set();
        let reactions = route.split('|'); // 获取单步的反应集合
        let length = reactions.length;  // length
        for (let i = 0; i < reactions.length; i++) {
          let single = reactions[i];
          let product = single.split('>')[0];
          let reactant = single.split('>')[2];
          mol_set.add(product);
          mol_set.add(reactant);
        }
        let tmp = Array.from(mol_set)
        let showRoute = tmp.join('——>')
        let perData = [i + 1, length, showRoute]

        // 创建tr,td
        let tr = document.createElement("tr");
        tbody.appendChild(tr);
        for (let k in perData) {
          let td = document.createElement("td");
          tr.appendChild(td);
          td.innerText = perData[k];
        }
      }
      // 将最优路径标记
      tbody.firstChild.style.color = '#17a2b8'
    }
  },
  mounted() {
    bus.$on('sendResultData', data => {
      this.resultData = data
      this.add();
    })
  }
}
</script>

<style scoped>

</style>
