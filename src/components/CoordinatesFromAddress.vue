<template>
  <div class="hello">
    <p>CoordinatesFromAddress</p>
    <p>Address</p>
    <input type="text" placeholder="Address" v-model="address" />
    <button @click="getCoordinates">Get coords</button>
    <p>Coords</p>
    {{coords.toString()}}
  </div>
</template>

<script>
import coordsService from '../services/coordsService'
export default {
  name: "CoordinatesFromAddress",
  props: {},
  data() {
    return {
      address: "",
      coords: ''
    };
  },
  methods: {
      async getCoordinates(){
          this.coords = await coordsService.getCoordsFromAddress(this.address)
      },

  }
};
</script>
