<template>
  <div style="margin-top: 30px">
    <!--  引言部分  -->
    <Intro></Intro>
    <!--   输入部分   -->
    <hr>
    <Input></Input>
    <hr>
    <!--   结果部分   -->
    <!--   展示部分   -->
    <Show></Show>
    <hr>
    <Result></Result>
</div>
</template>

<script>
import Input from "./Input";
import Result from "./Result";
import Intro from "./Intro";
import Show from "./Show";

export default {
  name: 'Retro',  //this is the name of the component
  components: {
    Input,
    Result,
    Intro,
    Show
  }
}
</script>

<style scoped>
hr {
  width: 80%;
}

</style>
