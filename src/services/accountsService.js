import api from '@/services/api'

export default {
  fetchAccounts() {
    return api.get(`accounts/`)
              .then(response => response.data)
  },
  updateLocation() {
    return api.put(`accounts/location`)
              .then(response => response.data)
  }
//   postMessage(payload) {
//     return api.post(`accounts/`, payload)
//               .then(response => response.data)
//   },
//   deleteMessage(msgId) {
//     return api.delete(`accounts/${msgId}`)
//               .then(response => response.data)
//   }
}