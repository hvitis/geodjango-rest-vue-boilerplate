<template>
  <div id="app">
    <h1>GeoDjango VueJs Leaflet Boilerplate</h1>
    <div id="nav">
     <router-link :to="{ name: 'home' }">Home</router-link> |
     <router-link :to="{ name: 'map' }">Map</router-link> |
     <router-link :to="{ name: 'address' }">Address</router-link> |
     <router-link :to="{ name: 'messages' }">Django Rest</router-link> |
     <router-link :to="{ name: 'ip' }">Location from IP</router-link> |
     <router-link :to="{ name: 'coords' }">Coords from address</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
