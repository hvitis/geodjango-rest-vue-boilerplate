<template>
  <div class="hello">
    <br/>
    <p>LocationFromIp</p>
    <button 
      value="Get Location" 
      @click="updateLocation()">
    </button>
    <hr/>
    <h3>Location</h3>
    {{acountLocation.toString()}}
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: "LocationFromIP",
  data() {
    return {};
  },
  computed: mapState({
    acountLocation: state => state.acountLocation
  }),
  methods: mapActions('accounts', [
    'updateLocation',
  ]),
  created() {
    this.$store.dispatch('messages/updateLocation')
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
