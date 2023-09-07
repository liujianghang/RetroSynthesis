<template>
  <div id="foot">
    <p>{{ msg }}</p>
  </div>
</template>
<script>
export default {
  name: "foot",
  data() {
    return {
      msg: "Copyright 2023",
    };
  },
};
</script>
<style scoped>
#foot {
  /*background:#F2F6FC;*/
  padding: 6px;
  border-radius: 5px;
  width: 80%;
  height: 80px;
  margin: 40px auto 20px;
}

p {
  color: #17a2b8;;
  text-align: center;
  margin: 30px auto;
  font-size: 1.1em;
}
</style>
