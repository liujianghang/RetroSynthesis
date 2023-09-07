<template>
  <div>
    <div class="main-bg">
      <div class="container ">
        <div class="my-background-img">
          <div class="content">
            <h1>Welcome!</h1>
            <p class="lead">You can get the retroynthesis pathways of the target molecule(SMILES) here！</p>
            <div class="my-text">
              <p>Here we develop BioRetro, a light and user-friendly platform which are capable of predicting the
                bioretrosynthesis pathways using a single-step bioretrosynthesis network, termed HybridMLP combined with
                AND-OR tree heuristic search.
                The HybridMLP utilizes a newly designed feature fusion network to fully extract the multiscale features
                of molecular descriptors to predict precursors that will produce the target NPs, while the AND-OR tree
                generates the iterative multi-step biosynthesis pathways with several heuristic
                strategies to select the better precursors to synthesis target.We have borrowed cytospace.js network
                graphic tool to clearly demonstrate the retroynthesis pathways. You can customize target molecules,
                iteration times and expansion during use. Please log in before use.

              </p>
            </div>
            <router-link to="/retro" class="btn btn-info my-btn" id="setup">Set up now</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Main"
}
</script>

<style scoped>
h1 {
  font-size: 75px;
}

@media (min-width: 1200px) {
  .container {
    max-width: 1400px;
  }
}

.my-background-img {
  margin-top: 10px;
  height: calc(70vh);
  /*background: url(../../../static/img/tiger.jpg) no-repeat;*/
  /*background-size: cover;*/
  position: relative;
  border-radius: 25px;
}

.content {
  line-height: 50px;
  font-size: 20px;
  height: calc(70vh);
  /*background: rgba(255, 255, 255, 0.75);*/
  text-align: center;
}

.lead {
  font-size: 30px;
  color: #008B8B;
}

#setup {
  border-radius: 10px;
}

.my-btn {
  font-size: 24px;
  margin-top: 40px;
  width: 200px;
  height: 60px;
}

.main-bg::after {
  background-color: #fef5e4;
  -webkit-border-radius: 0 0 233px 135px;
  -moz-border-radius: 0 0 233px 135px;
  border-radius: 0 0 233px 135px;
  content: "";
  position: absolute;
  right: -119px;
  top: -93px;
  background-color: #fef5e4;
  width: 466px;
  height: 595px;
  -webkit-transform: rotate(45deg);
  transform: rotate(116deg);
  z-index: -2;
}
</style>
