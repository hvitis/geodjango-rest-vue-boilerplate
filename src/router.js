import Vue from 'vue'
import Router from 'vue-router'
import MapPage from '@/components/MapPage'
import AddressSearch from '@/components/AddressSearch'
import Home from '@/pages/Home'
import Messages from '@/components/Messages'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/map',
      name: 'map',
      component: MapPage
    },
    {
      path: '/address',
      name: 'address',
      component: AddressSearch
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    }
  ]
})
