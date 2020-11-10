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
}