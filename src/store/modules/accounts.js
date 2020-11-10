import accountsService from '../../services/accountsService'

const state = {
  acountLocation: {}
}

const getters = {
    updateLocation: state => {
    return state.acountLocation
  }
}

const actions = {
  updateLocation ({ commit }) {
    accountsService.updateLocation()
    .then(location => {
      commit('acountLocation', location)
    })
  }
}

const mutations = {
    updateLocation (state, location) {
    state.acountLocation = location
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}