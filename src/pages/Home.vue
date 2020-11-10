<template>
  <div class="hello">
    <Info></Info>
  </div>
</template>

<script>
import Info from "../components/Info";
export default {
  name: "Home",
  props: {},
  components:{
      Info
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

img {
  width: 250px;
}
</style>
