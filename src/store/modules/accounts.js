import accountsService from "../../services/accountsService";

const state = {
  accountLocation: "",
};

const getters = {
  updateLocation: (state) => {
    return state.accountLocation;
  },
};

const actions = {
  updateLocation({ commit }) {
    accountsService
      .updateLocation()
      .then((response) => {
        let location = response.coordinates;
        commit("accountLocation", location);
      })
      .catch((error) => {
        let errorMessage = error.response.data.message
        commit("accountLocation", errorMessage);
      });
  },
};

const mutations = {
  accountLocation(state, location) {
    state.accountLocation = location;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
