import postService from '../../services/postsService'

const state = {
  posts: []
}

const getters = {
  posts: state => {
    return state.posts
  }
}

const actions = {
  getPosts ({ commit }) {
    postService.fetchPosts()
    .then(posts => {
      commit('setPosts', posts)
    })
  },
  addPost({ commit }, post) {
    postService.postMessage(post)
    .then(() => {
      commit('addPost', post)
    })
  },
  deletePost( { commit }, msgId) {
    postService.deletePost(msgId)
    commit('deletePost', msgId)
  }
}

const mutations = {
  setPosts (state, posts) {
    state.posts = posts
  },
  addPost(state, post) {
    state.posts.push(post)
  },
  deletePost(state, msgId) {
    state.posts = state.posts.filter(obj => obj.pk !== msgId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}