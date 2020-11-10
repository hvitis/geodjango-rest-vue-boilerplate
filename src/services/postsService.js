import api from '@/services/api'

export default {
  fetchPosts() {
    return api.get(`posts/`)
              .then(response => response.data)
  },
  postMessage(payload) {
    return api.post(`posts/`, payload)
              .then(response => response.data)
  },
  deleteMessage(msgId) {
    return api.delete(`posts/${msgId}`)
              .then(response => response.data)
  }
}