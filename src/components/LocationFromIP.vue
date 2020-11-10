<template>
  <div class="hello">
    <br/>
    <p>LocationFromIp</p>
    <button  
      @click="updateLocation()">
    Get Location</button>
    <hr/>
    <h3>Location:</h3>
    {{accountLocation}}
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: "LocationFromIP",
  data() {
    return {};
  },
  computed: {
    ...mapGetters({
      accountLocation: "accounts/updateLocation",
    
    }),
  },
  methods: mapActions('accounts', [
    'updateLocation',
  ]),
  created() {
    this.$store.dispatch('accounts/updateLocation')
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
hr {
  max-width: 65%;
}

.msg {
  margin: 0 auto;
  max-width: 30%;
  text-align: left;
  border-bottom: 1px solid #ccc;
  padding: 1rem;
}

.msg-index {
  color: #ccc;
  font-size: 0.8rem;
  /* margin-bottom: 0; */
}

img {
  width: 250px;
  padding-top: 50px;
  padding-bottom: 50px;
}

</style>
